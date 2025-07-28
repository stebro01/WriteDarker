import sys, os
import uuid
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_register_login_and_update():
    username = f"alice_{uuid.uuid4().hex[:6]}"
    resp = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": "secret",
            "first_name": "Alice",
            "last_name": "Doe",
            "age": 30,
            "email": f"{username}@example.com",
        },
    )
    assert resp.status_code == 200
    token_resp = client.post(
        "/auth/login",
        json={"username": username, "password": "secret"},
    )
    assert token_resp.status_code == 200
    token = token_resp.json()["access_token"]

    me_resp = client.get("/auth/me", params={"token": token})
    assert me_resp.status_code == 200
    assert me_resp.json()["username"] == username

    update_resp = client.put(
        "/auth/me",
        params={"token": token},
        json={"email": f"new_{username}@example.com"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["email"].startswith("new_")

    logout_resp = client.post("/auth/logout")
    assert logout_resp.status_code == 200
