import io
import os
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from backend.main import app


demo_pdf_path = Path(__file__).resolve().parent / "DEMO_DATA" / "PDF - Wikipedia.pdf"

client = TestClient(app)


def _register_and_login():
    """Utility that returns a fresh JWT token for a random user."""
    username = f"demo_{uuid4().hex[:8]}"
    password = "secret"
    # register
    resp = client.post("/auth/register", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    # login
    resp = client.post("/auth/login", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


def test_upload_demo_pdf():
    """Upload the sample Wikipedia PDF and ensure it appears in the user's reference list."""
    # Sanity – ensure the demo file exists inside the repo
    assert demo_pdf_path.exists(), f"Missing demo file at {demo_pdf_path}"

    token = _register_and_login()

    # Read PDF bytes and build multipart form-data
    with demo_pdf_path.open("rb") as fh:
        files = {"pdf": (demo_pdf_path.name, fh, "application/pdf")}
        data = {"query": demo_pdf_path.name}  # simple query equals filename
        # Note: no project_ids → should succeed regardless of projects
        resp = client.post("/references/", params={"token": token}, data=data, files=files)

    assert resp.status_code == 200, resp.text
    ref_id = resp.json()["id"]

    # Verify the reference is returned when listing all references for the user
    resp = client.get("/references/user", params={"token": token})
    assert resp.status_code == 200, resp.text
    refs = resp.json()
    ids = {r["id"] for r in refs}
    assert ref_id in ids

    uploaded = next(r for r in refs if r["id"] == ref_id)
    assert uploaded["filename"] == demo_pdf_path.name
    assert uploaded["filetype"].startswith("application/pdf")
