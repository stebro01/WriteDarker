import io
from uuid import uuid4
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def _register_and_login():
    """Utility that returns a fresh JWT token for a random user."""
    username = f"delete_test_{uuid4().hex[:8]}"
    password = "secret"
    # register
    resp = client.post("/auth/register", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    # login
    resp = client.post("/auth/login", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


def test_delete_reference_single_user():
    """Test deleting a reference when only one user has access."""
    token = _register_and_login()
    
    # Upload a reference
    pdf_content = b"test pdf content"
    files = {"pdf": ("test.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"query": "Test Reference"}
    resp = client.post("/references/", params={"token": token}, data=data, files=files)
    assert resp.status_code == 200, resp.text
    ref_id = resp.json()["id"]
    
    # Verify reference exists
    resp = client.get("/references/user", params={"token": token})
    assert resp.status_code == 200, resp.text
    assert len(resp.json()) == 1
    assert resp.json()[0]["id"] == ref_id
    
    # Delete the reference
    resp = client.delete(f"/references/{ref_id}", params={"token": token})
    assert resp.status_code == 200, resp.text
    assert resp.json()["message"] == "deleted"
    
    # Verify reference is completely deleted
    resp = client.get("/references/user", params={"token": token})
    assert resp.status_code == 200, resp.text
    assert len(resp.json()) == 0


def test_delete_reference_multiple_users():
    """Test deleting a reference when multiple users have access."""
    # Create two users
    token1 = _register_and_login()
    token2 = _register_and_login()
    
    # User 1 uploads a reference
    pdf_content = b"shared pdf content"
    files = {"pdf": ("shared.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"query": "Shared Reference"}
    resp = client.post("/references/", params={"token": token1}, data=data, files=files)
    assert resp.status_code == 200, resp.text
    ref_id = resp.json()["id"]
    
    # User 2 uploads the same file (should get access to existing reference)
    resp = client.post("/references/", params={"token": token2}, data=data, files=files)
    assert resp.status_code == 200, resp.text
    # Should return the same reference ID
    assert resp.json()["id"] == ref_id
    
    # Verify both users can see the reference
    resp1 = client.get("/references/user", params={"token": token1})
    resp2 = client.get("/references/user", params={"token": token2})
    assert resp1.status_code == 200, resp1.text
    assert resp2.status_code == 200, resp2.text
    assert len(resp1.json()) == 1
    assert len(resp2.json()) == 1
    assert resp1.json()[0]["id"] == ref_id
    assert resp2.json()[0]["id"] == ref_id
    
    # User 1 deletes the reference (should only remove their access)
    resp = client.delete(f"/references/{ref_id}", params={"token": token1})
    assert resp.status_code == 200, resp.text
    assert resp.json()["message"] == "deleted"
    
    # Verify user 1 no longer has access
    resp1 = client.get("/references/user", params={"token": token1})
    assert resp1.status_code == 200, resp1.text
    assert len(resp1.json()) == 0
    
    # Verify user 2 still has access
    resp2 = client.get("/references/user", params={"token": token2})
    assert resp2.status_code == 200, resp2.text
    assert len(resp2.json()) == 1
    assert resp2.json()[0]["id"] == ref_id
    
    # User 2 deletes the reference (should completely delete it)
    resp = client.delete(f"/references/{ref_id}", params={"token": token2})
    assert resp.status_code == 200, resp.text
    assert resp.json()["message"] == "deleted"
    
    # Verify reference is completely deleted
    resp2 = client.get("/references/user", params={"token": token2})
    assert resp2.status_code == 200, resp2.text
    assert len(resp2.json()) == 0


def test_delete_nonexistent_reference():
    """Test deleting a reference that doesn't exist."""
    token = _register_and_login()
    
    # Try to delete a non-existent reference
    resp = client.delete("/references/99999", params={"token": token})
    assert resp.status_code == 404, resp.text


def test_delete_unauthorized_reference():
    """Test deleting a reference that the user doesn't have access to."""
    token1 = _register_and_login()
    token2 = _register_and_login()
    
    # User 1 uploads a reference
    pdf_content = b"private pdf content"
    files = {"pdf": ("private.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"query": "Private Reference"}
    resp = client.post("/references/", params={"token": token1}, data=data, files=files)
    assert resp.status_code == 200, resp.text
    ref_id = resp.json()["id"]
    
    # User 2 tries to delete it (should fail)
    resp = client.delete(f"/references/{ref_id}", params={"token": token2})
    assert resp.status_code == 404, resp.text
    
    # Verify user 1 still has access
    resp = client.get("/references/user", params={"token": token1})
    assert resp.status_code == 200, resp.text
    assert len(resp.json()) == 1
    assert resp.json()[0]["id"] == ref_id 