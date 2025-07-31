import sys, os
import uuid
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def get_token():
    username = f"user_{uuid.uuid4().hex[:6]}"
    client.post(
        "/auth/register",
        json={"username": username, "password": "secret"},
    )
    resp = client.post("/auth/login", json={"username": username, "password": "secret"})
    return resp.json()["access_token"]


def test_create_update_delete_project():
    token = get_token()
    create_resp = client.post(
        "/projects/",
        params={"token": token},
        json={"label": "Test", "description": "desc", "coauthors": "bob"},
    )
    assert create_resp.status_code == 200
    proj = create_resp.json()
    pid = proj["id"]

    read_resp = client.get(f"/projects/{pid}", params={"token": token})
    assert read_resp.status_code == 200

    upd_resp = client.put(
        f"/projects/{pid}",
        params={"token": token},
        json={"description": "new"},
    )
    assert upd_resp.status_code == 200
    assert upd_resp.json()["description"] == "new"

    del_resp = client.delete(f"/projects/{pid}", params={"token": token})
    assert del_resp.status_code == 200


def test_list_projects_with_summary():
    token = get_token()
    create_resp = client.post(
        "/projects/",
        params={"token": token},
        json={"label": "Test", "description": "desc"},
    )
    assert create_resp.status_code == 200
    proj = create_resp.json()
    pid = proj["id"]
    # create documents
    client.post(
        "/documents/",
        params={"token": token, "text": "hello world", "project_id": pid},
    )
    client.post(
        "/documents/",
        params={"token": token, "text": "second doc", "project_id": pid},
    )
    list_resp = client.get("/projects/", params={"token": token})
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert isinstance(data, list)
    assert len(data) == 1
    summary = data[0]
    assert summary["document_count"] == 2
    assert summary["word_count"] == 4
    assert summary["reference_count"] == 0
    assert summary["media_count"] == 0
