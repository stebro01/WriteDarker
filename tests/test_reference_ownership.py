import io
from uuid import uuid4
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def _register_and_login():
    """Utility that returns a fresh JWT token for a random user."""
    username = f"ownership_{uuid4().hex[:8]}"
    password = "secret"
    # register
    resp = client.post("/auth/register", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    # login
    resp = client.post("/auth/login", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


def test_reference_ownership_via_junction_table():
    """Test that references are properly managed via reference_to_owner table."""
    token1 = _register_and_login()
    token2 = _register_and_login()
    
    # User 1 creates a reference
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 1\n0000000000 65535 f \ntrailer\n<<\n/Size 1\n/Root 1 0 R\n>>\nstartxref\n9\n%%EOF"
    files = {"pdf": ("ownership_test.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"query": "Ownership Test Document"}
    resp1 = client.post("/references/", params={"token": token1}, data=data, files=files)
    assert resp1.status_code == 200, resp1.text
    ref_id = resp1.json()["id"]
    
    # User 1 should see the reference
    resp = client.get("/references/user", params={"token": token1})
    assert resp.status_code == 200
    refs = resp.json()
    assert len(refs) >= 1
    assert any(r["id"] == ref_id for r in refs)
    
    # User 2 should not see the reference
    resp = client.get("/references/user", params={"token": token2})
    assert resp.status_code == 200
    refs = resp.json()
    assert not any(r["id"] == ref_id for r in refs)
    
    # User 2 uploads the same file - should get shared access
    files = {"pdf": ("ownership_test_copy.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"query": "Ownership Test Document Copy"}
    resp2 = client.post("/references/", params={"token": token2}, data=data, files=files)
    assert resp2.status_code == 200, resp2.text
    # Should return the same reference ID (shared)
    assert resp2.json()["id"] == ref_id
    
    # Now both users should see the reference
    resp = client.get("/references/user", params={"token": token1})
    assert resp.status_code == 200
    refs1 = resp.json()
    assert any(r["id"] == ref_id for r in refs1)
    
    resp = client.get("/references/user", params={"token": token2})
    assert resp.status_code == 200
    refs2 = resp.json()
    assert any(r["id"] == ref_id for r in refs2)


def test_reference_deletion_behavior():
    """Test that deleting removes user access and deletes reference if no users left."""
    token1 = _register_and_login()
    token2 = _register_and_login()
    
    # User 1 creates a reference
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 1\n0000000000 65535 f \ntrailer\n<<\n/Size 1\n/Root 1 0 R\n>>\nstartxref\n9\n%%EOF"
    files = {"pdf": ("delete_test.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"query": "Delete Test Document"}
    resp1 = client.post("/references/", params={"token": token1}, data=data, files=files)
    assert resp1.status_code == 200, resp1.text
    ref_id = resp1.json()["id"]
    
    # User 2 uploads same file - gets shared access
    files = {"pdf": ("delete_test_copy.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"query": "Delete Test Document Copy"}
    resp2 = client.post("/references/", params={"token": token2}, data=data, files=files)
    assert resp2.status_code == 200, resp2.text
    assert resp2.json()["id"] == ref_id
    
    # Both users have access
    resp = client.get("/references/user", params={"token": token1})
    assert any(r["id"] == ref_id for r in resp.json())
    resp = client.get("/references/user", params={"token": token2})
    assert any(r["id"] == ref_id for r in resp.json())
    
    # User 1 deletes their access
    resp = client.delete(f"/references/{ref_id}", params={"token": token1})
    assert resp.status_code == 200
    
    # User 1 should no longer see the reference
    resp = client.get("/references/user", params={"token": token1})
    assert not any(r["id"] == ref_id for r in resp.json())
    
    # User 2 should still see the reference
    resp = client.get("/references/user", params={"token": token2})
    assert any(r["id"] == ref_id for r in resp.json())
    
    # User 2 deletes their access - should delete the reference entirely
    resp = client.delete(f"/references/{ref_id}", params={"token": token2})
    assert resp.status_code == 200
    
    # Neither user should see the reference now
    resp = client.get("/references/user", params={"token": token1})
    assert not any(r["id"] == ref_id for r in resp.json())
    resp = client.get("/references/user", params={"token": token2})
    assert not any(r["id"] == ref_id for r in resp.json())
    
    # Trying to access the reference should return 404
    resp = client.get(f"/references/{ref_id}", params={"token": token1})
    assert resp.status_code == 404
    resp = client.get(f"/references/{ref_id}", params={"token": token2})
    assert resp.status_code == 404


def test_single_user_reference_deletion():
    """Test that when a single user deletes a reference, it's completely removed."""
    token = _register_and_login()
    
    # Create a reference
    data = {"query": "Single User Test"}
    resp = client.post("/references/", params={"token": token}, data=data)
    assert resp.status_code == 200, resp.text
    ref_id = resp.json()["id"]
    
    # User should see the reference
    resp = client.get("/references/user", params={"token": token})
    assert any(r["id"] == ref_id for r in resp.json())
    
    # Delete the reference
    resp = client.delete(f"/references/{ref_id}", params={"token": token})
    assert resp.status_code == 200
    
    # Reference should be completely gone
    resp = client.get("/references/user", params={"token": token})
    assert not any(r["id"] == ref_id for r in resp.json())
    
    resp = client.get(f"/references/{ref_id}", params={"token": token})
    assert resp.status_code == 404