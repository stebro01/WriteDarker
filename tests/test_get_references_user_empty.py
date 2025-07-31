from fastapi.testclient import TestClient
from backend.main import app
from uuid import uuid4

def test_empty_user_refs():
    client = TestClient(app)
    # register + login
    username=f"u_{uuid4().hex[:6]}"
    passwd="secret"
    resp=client.post("/auth/register", json={"username":username, "password": passwd})
    assert resp.status_code==200
    resp=client.post("/auth/login", json={"username":username, "password": passwd})
    token=resp.json()["access_token"]
    resp=client.get("/references/user", params={"token": token})
    assert resp.status_code==200
    assert resp.json()==[]
