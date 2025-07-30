import io
import uuid
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from PyPDF2 import PdfWriter
from backend.main import app

client = TestClient(app)


def create_user_and_token():
    username = f"wf_{uuid.uuid4().hex[:6]}"
    client.post(
        "/auth/register",
        json={"username": username, "password": "secret"},
    )
    resp = client.post("/auth/login", json={"username": username, "password": "secret"})
    return resp.json()["access_token"]


def test_full_workflow():
    token = create_user_and_token()

    # create project
    proj_resp = client.post(
        "/projects/",
        params={"token": token},
        json={"label": "WF", "description": "workflow"},
    )
    assert proj_resp.status_code == 200
    project_id = proj_resp.json()["id"]

    # create documents in project
    doc1_resp = client.post(
        "/documents/",
        params={"token": token, "project_id": project_id, "text": "doc1", "position": 0},
    )
    assert doc1_resp.status_code == 200
    doc1_id = doc1_resp.json()["id"]

    doc2_resp = client.post(
        "/documents/",
        params={"token": token, "project_id": project_id, "text": "doc2", "position": 1},
    )
    assert doc2_resp.status_code == 200
    doc2_id = doc2_resp.json()["id"]

    # reorder documents
    upd_resp = client.put(
        f"/documents/{doc2_id}",
        params={"token": token},
        json={"position": 0},
    )
    assert upd_resp.status_code == 200

    client.put(
        f"/documents/{doc1_id}",
        params={"token": token},
        json={"position": 1},
    )

    list_resp = client.get(f"/documents/project/{project_id}", params={"token": token})
    assert list_resp.status_code == 200
    docs = list_resp.json()
    assert len(docs) == 2
    assert docs[0]["id"] == doc2_id

    # add reference with pdf
    pdf_buf = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.write(pdf_buf)
    pdf_buf.seek(0)
    files = {"pdf": ("ref.pdf", pdf_buf, "application/pdf")}
    ref_resp = client.post(
        "/references/",
        params={"token": token},
        data={"query": "test", "project_ids": str(project_id)},
        files=files,
    )
    assert ref_resp.status_code == 200
    ref_id = ref_resp.json()["id"]

    get_ref = client.get(f"/references/{ref_id}", params={"token": token})
    assert get_ref.status_code == 200
    assert get_ref.json()["title"] == "test"
