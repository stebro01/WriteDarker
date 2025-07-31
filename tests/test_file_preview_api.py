import io
from pathlib import Path
from uuid import uuid4
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def _register_and_login():
    """Utility that returns a fresh JWT token for a random user."""
    username = f"preview_{uuid4().hex[:8]}"
    password = "secret"
    # register
    resp = client.post("/auth/register", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    # login
    resp = client.post("/auth/login", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


def test_preview_text_file():
    """Test previewing a text file."""
    token = _register_and_login()
    
    # Upload a text file
    text_content = b"This is a test text file.\nWith multiple lines.\nFor preview testing."
    files = {"pdf": ("test.txt", io.BytesIO(text_content), "text/plain")}
    data = {"query": "Test Text File"}
    resp = client.post("/references/", params={"token": token}, data=data, files=files)
    assert resp.status_code == 200, resp.text
    ref_id = resp.json()["id"]
    
    # Preview the file
    resp = client.get(f"/references/{ref_id}/file", params={"token": token})
    assert resp.status_code == 200
    assert resp.content == text_content
    assert resp.headers["content-type"] == "text/plain; charset=utf-8"


def test_preview_json_file():
    """Test previewing a JSON file."""
    token = _register_and_login()
    
    # Upload a JSON file
    json_content = b'{"name": "test", "value": 123, "nested": {"key": "value"}}'
    files = {"pdf": ("test.json", io.BytesIO(json_content), "application/json")}
    data = {"query": "Test JSON File"}
    resp = client.post("/references/", params={"token": token}, data=data, files=files)
    assert resp.status_code == 200, resp.text
    ref_id = resp.json()["id"]
    
    # Preview the file
    resp = client.get(f"/references/{ref_id}/file", params={"token": token})
    assert resp.status_code == 200
    assert resp.content == json_content
    assert "application/json" in resp.headers["content-type"]


def test_preview_pdf_file():
    """Test previewing a PDF file."""
    token = _register_and_login()
    
    # Upload a simple PDF
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 1\n0000000000 65535 f \ntrailer\n<<\n/Size 1\n/Root 1 0 R\n>>\nstartxref\n9\n%%EOF"
    files = {"pdf": ("test.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"query": "Test PDF File"}
    resp = client.post("/references/", params={"token": token}, data=data, files=files)
    assert resp.status_code == 200, resp.text
    ref_id = resp.json()["id"]
    
    # Preview the file
    resp = client.get(f"/references/{ref_id}/file", params={"token": token})
    assert resp.status_code == 200
    assert resp.content == pdf_content
    assert resp.headers["content-type"] == "application/pdf"
    assert "inline" in resp.headers["content-disposition"]


def test_preview_nonexistent_reference():
    """Test previewing a non-existent reference."""
    token = _register_and_login()
    
    # Try to preview a non-existent reference
    resp = client.get("/references/99999/file", params={"token": token})
    assert resp.status_code == 404


def test_preview_unauthorized_access():
    """Test that users can't preview files they don't have access to."""
    token1 = _register_and_login()
    token2 = _register_and_login()
    
    # User 1 uploads a file
    text_content = b"Private file content"
    files = {"pdf": ("private.txt", io.BytesIO(text_content), "text/plain")}
    data = {"query": "Private File"}
    resp = client.post("/references/", params={"token": token1}, data=data, files=files)
    assert resp.status_code == 200, resp.text
    ref_id = resp.json()["id"]
    
    # User 2 tries to preview it (should fail)
    resp = client.get(f"/references/{ref_id}/file", params={"token": token2})
    assert resp.status_code == 404  # Should not find the reference


def test_preview_reference_without_file():
    """Test previewing a reference that has no file content."""
    token = _register_and_login()
    
    # Create a reference without a file
    data = {"query": "No File Reference"}
    resp = client.post("/references/", params={"token": token}, data=data)
    assert resp.status_code == 200, resp.text
    ref_id = resp.json()["id"]
    
    # Try to preview (should fail)
    resp = client.get(f"/references/{ref_id}/file", params={"token": token})
    assert resp.status_code == 404
    assert "No file content available" in resp.json()["detail"]