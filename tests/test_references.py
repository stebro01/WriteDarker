import uuid
from unittest.mock import patch
import io
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def get_token():
    username = f"refu_{uuid.uuid4().hex[:6]}"
    client.post("/auth/register", json={"username": username, "password": "secret"})
    resp = client.post("/auth/login", json={"username": username, "password": "secret"})
    return resp.json()["access_token"]


def test_list_filter_and_delete_references():
    token = get_token()
    proj_resp = client.post(
        "/projects/",
        params={"token": token},
        json={"label": "Refs", "description": "test"},
    )
    assert proj_resp.status_code == 200
    proj_id = proj_resp.json()["id"]

    def fake_fetch(q):
        return {"title": q, "authors": "", "journal": "", "year": "2024"}

    with patch("backend.api.references.ref_service.fetch_reference", side_effect=fake_fetch):
        ref1 = client.post(
            "/references/",
            params={"token": token},
            data={"query": "alpha", "project_ids": str(proj_id)},
        ).json()
        ref2 = client.post(
            "/references/",
            params={"token": token},
            data={"query": "beta", "project_ids": str(proj_id)},
        ).json()
        ref3 = client.post(
            "/references/",
            params={"token": token},
            data={"query": "gamma"},
        ).json()

    list_resp = client.get("/references/user", params={"token": token})
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 3

    search_resp = client.get("/references/user", params={"token": token, "search": "beta"})
    assert search_resp.status_code == 200
    data = search_resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "beta"

    sort_resp = client.get("/references/user", params={"token": token, "sort": "-title"})
    assert sort_resp.status_code == 200
    titles = [r["title"] for r in sort_resp.json()]
    assert titles == sorted([ref1["title"], ref2["title"], ref3["title"]], reverse=True)

    del_resp = client.delete(f"/references/{ref2['id']}", params={"token": token})
    assert del_resp.status_code == 200

    get_resp = client.get(f"/references/{ref2['id']}", params={"token": token})
    assert get_resp.status_code == 404


def test_upload_list_and_delete_reference_files():
    token = get_token()
    proj_resp = client.post(
        "/projects/",
        params={"token": token},
        json={"label": "FileRefs", "description": "test"},
    )
    assert proj_resp.status_code == 200
    proj_id = proj_resp.json()["id"]

    def fake_fetch(q):
        return {"title": q, "authors": "", "journal": "", "year": "2024"}

    with patch("backend.api.references.ref_service.fetch_reference", side_effect=fake_fetch):
        pdf_buf = io.BytesIO(b"%PDF-1.4")
        pdf_resp = client.post(
            "/references/",
            params={"token": token},
            data={"query": "pdfref", "project_ids": str(proj_id)},
            files={"pdf": ("paper.pdf", pdf_buf, "application/pdf")},
        )
        assert pdf_resp.status_code == 200
        pdf_id = pdf_resp.json()["id"]

        txt_buf = io.BytesIO(b"some text")
        txt_resp = client.post(
            "/references/",
            params={"token": token},
            data={"query": "txtref", "project_ids": str(proj_id)},
            files={"pdf": ("notes.txt", txt_buf, "text/plain")},
        )
        assert txt_resp.status_code == 200
        txt_id = txt_resp.json()["id"]

    proj_list = client.get(f"/references/project/{proj_id}", params={"token": token})
    assert proj_list.status_code == 200
    assert len(proj_list.json()) == 2

    user_list = client.get("/references/user", params={"token": token})
    assert user_list.status_code == 200
    assert len(user_list.json()) == 2
    by_title = {r["title"]: r for r in user_list.json()}
    assert by_title["pdfref"]["filename"] == "paper.pdf"
    assert by_title["pdfref"]["filetype"] == "application/pdf"
    assert by_title["txtref"]["filename"] == "notes.txt"
    assert by_title["txtref"]["filetype"] == "text/plain"

    del_resp = client.delete(f"/references/{txt_id}", params={"token": token})
    assert del_resp.status_code == 200
    get_resp = client.get(f"/references/{txt_id}", params={"token": token})
    assert get_resp.status_code == 404

    client.delete(f"/references/{pdf_id}", params={"token": token})

