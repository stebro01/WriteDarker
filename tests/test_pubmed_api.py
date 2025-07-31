import sys, os
import uuid
from unittest.mock import patch
import httpx
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

SAMPLE_XML = """<?xml version='1.0' encoding='UTF-8'?>
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <Article>
        <Journal>
          <JournalIssue>
            <PubDate>
              <Year>2024</Year>
            </PubDate>
          </JournalIssue>
          <ISOAbbreviation>J Neurol</ISOAbbreviation>
        </Journal>
        <ArticleTitle>Persistent cognitive slowing in post-COVID patients: longitudinal study over 6 months.</ArticleTitle>
        <AuthorList>
          <Author><LastName>Martin</LastName><Initials>EM</Initials></Author>
          <Author><LastName>Srowig</LastName><Initials>A</Initials></Author>
          <Author><LastName>Utech</LastName><Initials>I</Initials></Author>
          <Author><LastName>Schrenk</LastName><Initials>S</Initials></Author>
          <Author><LastName>Kattlun</LastName><Initials>F</Initials></Author>
          <Author><LastName>Radscheidt</LastName><Initials>M</Initials></Author>
          <Author><LastName>Brodoehl</LastName><Initials>S</Initials></Author>
          <Author><LastName>Bublak</LastName><Initials>P</Initials></Author>
          <Author><LastName>Schwab</LastName><Initials>M</Initials></Author>
          <Author><LastName>Geis</LastName><Initials>C</Initials></Author>
          <Author><LastName>Besteher</LastName><Initials>B</Initials></Author>
          <Author><LastName>Reuken</LastName><Initials>PA</Initials></Author>
          <Author><LastName>Stallmach</LastName><Initials>A</Initials></Author>
          <Author><LastName>Finke</LastName><Initials>K</Initials></Author>
        </AuthorList>
      </Article>
    </MedlineCitation>
  </PubmedArticle>
</PubmedArticleSet>"""

class FakeResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP error")


def mock_get(url, timeout=10):
    return FakeResponse(SAMPLE_XML)


def get_token():
    username = f"ref_{uuid.uuid4().hex[:6]}"
    client.post("/auth/register", json={"username": username, "password": "secret"})
    resp = client.post("/auth/login", json={"username": username, "password": "secret"})
    return resp.json()["access_token"]


def test_fetch_pubmed_reference_and_store():
    token = get_token()
    proj_resp = client.post(
        "/projects/",
        params={"token": token},
        json={"label": "Ref", "description": "test"},
    )
    assert proj_resp.status_code == 200
    proj_id = proj_resp.json()["id"]

    with patch("backend.services.references.httpx.get", side_effect=mock_get):
        resp = client.post(
            "/references/",
            params={"token": token},
            data={"project_id": proj_id, "query": "37936010"},
        )

    assert resp.status_code == 200
    ref = resp.json()
    assert ref["title"] == "Persistent cognitive slowing in post-COVID patients: longitudinal study over 6 months."
    assert ref["authors"].startswith("Martin EM")
    assert ref["authors"].endswith("Finke K")
    assert ref["journal"] == "J Neurol"
    assert ref["year"] == "2024"

    get_resp = client.get(f"/references/{ref['id']}", params={"token": token})
    assert get_resp.status_code == 200
    assert get_resp.json() == ref


def test_fetch_pubmed_reference_network_error():
    token = get_token()
    proj_resp = client.post(
        "/projects/",
        params={"token": token},
        json={"label": "Ref", "description": "test"},
    )
    assert proj_resp.status_code == 200
    proj_id = proj_resp.json()["id"]

    def raise_error(url, timeout=10):
        raise httpx.HTTPError("boom")

    with patch("backend.services.references.httpx.get", side_effect=raise_error):
        resp = client.post(
            "/references/",
            params={"token": token},
            data={"project_id": proj_id, "query": "37936010"},
        )

    assert resp.status_code == 200
    ref = resp.json()
    assert ref == {
        "id": ref["id"],
        "title": "37936010",
        "authors": "",
        "journal": "",
        "year": "",
        "filename": None,
        "filetype": None,
        "file_hash": None,
    }
