import sys, os
import io
import uuid
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from PyPDF2 import PdfWriter
from backend.main import app

client = TestClient(app)


def get_token():
    username = f"bob_{uuid.uuid4().hex[:6]}"
    client.post(
        "/auth/register",
        json={"username": username, "password": "secret", "email": f"{username}@example.com"},
    )
    resp = client.post("/auth/login", json={"username": username, "password": "secret"})
    return resp.json()["access_token"]


def test_create_read_delete_document():
    token = get_token()
    create_resp = client.post(
        "/documents/",
        params={"token": token, "text": "hello world"},
    )
    assert create_resp.status_code == 200
    doc_id = create_resp.json()["id"]

    read_resp = client.get(f"/documents/{doc_id}", params={"token": token})
    assert read_resp.status_code == 200
    assert read_resp.json()["text"] == "hello world"

    del_resp = client.delete(f"/documents/{doc_id}", params={"token": token})
    assert del_resp.status_code == 200


def test_upload_pdf():
    token = get_token()
    pdf_buf = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.write(pdf_buf)
    pdf_buf.seek(0)
    files = {"pdf": ("test.pdf", pdf_buf, "application/pdf")}
    resp = client.post("/documents/", params={"token": token}, files=files)
    assert resp.status_code == 200
    assert resp.json()["id"] is not None


def test_revision_history_and_restore():
    token = get_token()
    # create document
    resp = client.post("/documents/", params={"token": token, "text": "v1"})
    assert resp.status_code == 200
    doc_id = resp.json()["id"]

    # update twice
    resp = client.put(f"/documents/{doc_id}", params={"token": token}, json={"text": "v2"})
    assert resp.status_code == 200
    resp = client.put(f"/documents/{doc_id}", params={"token": token}, json={"text": "v3"})
    assert resp.status_code == 200

    # check revisions
    rev_resp = client.get(f"/documents/{doc_id}/revisions", params={"token": token})
    assert rev_resp.status_code == 200
    revs = rev_resp.json()
    assert len(revs) == 2

    # restore first revision
    restore_resp = client.post(
        f"/documents/{doc_id}/restore/{revs[0]['id']}", params={"token": token}
    )
    assert restore_resp.status_code == 200
    assert restore_resp.json()["text"] == "v1"

    # ensure revision added
    rev_resp2 = client.get(f"/documents/{doc_id}/revisions", params={"token": token})
    assert rev_resp2.status_code == 200
    assert len(rev_resp2.json()) == 3
