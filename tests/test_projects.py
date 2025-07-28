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
