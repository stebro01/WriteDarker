import io
import os
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def _register_and_login():
    """Utility that returns a fresh JWT token for a random user."""
    username = f"hashtest_{uuid4().hex[:8]}"
    password = "secret"
    # register
    resp = client.post("/auth/register", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    # login
    resp = client.post("/auth/login", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


def test_duplicate_file_detection():
    """Test that uploading the same file twice results in a 409 error."""
    token = _register_and_login()
    
    # Create a test PDF content
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 1\n0000000000 65535 f \ntrailer\n<<\n/Size 1\n/Root 1 0 R\n>>\nstartxref\n9\n%%EOF"
    
    # First upload should succeed
    files = {"pdf": ("test.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"query": "Test Document"}
    resp1 = client.post("/references/", params={"token": token}, data=data, files=files)
    assert resp1.status_code == 200, resp1.text
    ref1 = resp1.json()
    assert ref1["filename"] == "test.pdf"
    assert ref1["file_hash"] is not None
    
    # Second upload of same file should fail with 409
    files = {"pdf": ("test_copy.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"query": "Test Document Copy"}
    resp2 = client.post("/references/", params={"token": token}, data=data, files=files)
    assert resp2.status_code == 409, resp2.text
    assert "already exists" in resp2.json()["detail"]


def test_different_files_allowed():
    """Test that uploading different files is allowed."""
    token = _register_and_login()
    
    # Create two different PDF contents
    pdf_content1 = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 1\n0000000000 65535 f \ntrailer\n<<\n/Size 1\n/Root 1 0 R\n>>\nstartxref\n9\n%%EOF"
    pdf_content2 = b"%PDF-1.4\n2 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 1\n0000000000 65535 f \ntrailer\n<<\n/Size 2\n/Root 2 0 R\n>>\nstartxref\n9\n%%EOF"
    
    # First upload
    files = {"pdf": ("unique1.pdf", io.BytesIO(pdf_content1), "application/pdf")}
    data = {"query": "Unique Document 1"}
    resp1 = client.post("/references/", params={"token": token}, data=data, files=files)
    assert resp1.status_code == 200, resp1.text
    ref1 = resp1.json()
    
    # Second upload with different content should succeed
    files = {"pdf": ("unique2.pdf", io.BytesIO(pdf_content2), "application/pdf")}
    data = {"query": "Unique Document 2"}
    resp2 = client.post("/references/", params={"token": token}, data=data, files=files)
    assert resp2.status_code == 200, resp2.text
    ref2 = resp2.json()
    
    # Should have different hashes
    assert ref1["file_hash"] != ref2["file_hash"]
    
    # Both should appear in user's references
    resp = client.get("/references/user", params={"token": token})
    assert resp.status_code == 200
    refs = resp.json()
    
    # Should have at least 2 references for this user
    assert len(refs) >= 2
    
    # Find our specific references by their IDs
    ref1_found = any(r["id"] == ref1["id"] for r in refs)
    ref2_found = any(r["id"] == ref2["id"] for r in refs)
    assert ref1_found and ref2_found


def test_file_sharing_between_users():
    """Test that when a second user uploads the same file, it gets shared."""
    token1 = _register_and_login()
    token2 = _register_and_login()
    
    # Create a test PDF content
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 1\n0000000000 65535 f \ntrailer\n<<\n/Size 1\n/Root 1 0 R\n>>\nstartxref\n9\n%%EOF"
    
    # User 1 uploads file
    files = {"pdf": ("shared.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"query": "Shared Document"}
    resp1 = client.post("/references/", params={"token": token1}, data=data, files=files)
    assert resp1.status_code == 200, resp1.text
    ref1 = resp1.json()
    
    # User 2 uploads same file - should get shared access to existing reference
    files = {"pdf": ("shared.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"query": "Shared Document"}
    resp2 = client.post("/references/", params={"token": token2}, data=data, files=files)
    assert resp2.status_code == 200, resp2.text
    ref2 = resp2.json()
    
    # Should be the same reference (same ID)
    assert ref1["id"] == ref2["id"]
    assert ref1["file_hash"] == ref2["file_hash"]
    
    # Both users should see it in their reference lists
    resp1_list = client.get("/references/user", params={"token": token1})
    assert resp1_list.status_code == 200
    user1_refs = resp1_list.json()
    assert len(user1_refs) == 1
    assert user1_refs[0]["id"] == ref1["id"]
    
    resp2_list = client.get("/references/user", params={"token": token2})
    assert resp2_list.status_code == 200
    user2_refs = resp2_list.json()
    assert len(user2_refs) == 1
    assert user2_refs[0]["id"] == ref1["id"]


def test_no_file_upload_works():
    """Test that references without files still work (no hash)."""
    token = _register_and_login()
    
    # Upload reference without file
    data = {"query": "Text Only Reference"}
    resp = client.post("/references/", params={"token": token}, data=data)
    assert resp.status_code == 200, resp.text
    ref = resp.json()
    assert ref["filename"] is None
    assert ref["file_hash"] is None
    
    # Should appear in user's references
    resp = client.get("/references/user", params={"token": token})
    assert resp.status_code == 200
    refs = resp.json()
    assert len(refs) == 1
    assert refs[0]["title"] == "Text Only Reference"