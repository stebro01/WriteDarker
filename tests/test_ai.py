import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_mcp_endpoint_returns_mock_response():
    resp = client.post("/ai/mcp", json={"prompt": "hello"})
    assert resp.status_code == 200
    data = resp.json()
    assert "response" in data
    assert isinstance(data["response"], str)
    assert "hello" in data["response"]
