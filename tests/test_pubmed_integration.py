"""Comprehensive tests for PubMed API integration."""

import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4
import io
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def _register_and_login():
    """Utility that returns a fresh JWT token for a random user."""
    username = f"pubmed_{uuid4().hex[:8]}"
    password = "secret"
    # register
    resp = client.post("/auth/register", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    # login
    resp = client.post("/auth/login", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


@patch('backend.services.pubmed.pubmed_service.search_articles')
def test_pubmed_search_success(mock_search):
    """Test successful PubMed search."""
    token = _register_and_login()
    
    # Mock successful response
    mock_search.return_value = [
        {
            'pubmed_id': '12345678',
            'title': 'Test Article',
            'abstract': 'This is a test abstract.',
            'authors': 'Smith, J.; Doe, A.',
            'journal': 'Test Journal',
            'publication_date': '2023-01-01',
            'doi': '10.1234/test',
            'keywords': ['machine learning', 'AI'],
            'url': 'https://pubmed.ncbi.nlm.nih.gov/12345678',
            'citation': 'Smith, J.; Doe, A. Test Article. Test Journal. 2023-01-01.'
        }
    ]
    
    resp = client.post(
        "/pubmed/search",
        json={"query": "machine learning", "max_results": 5},
        params={"token": token}
    )
    
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_results"] == 1
    assert len(data["articles"]) == 1
    
    article = data["articles"][0]
    assert article["pubmed_id"] == "12345678"
    assert article["title"] == "Test Article"
    assert article["authors"] == "Smith, J.; Doe, A."
    assert article["journal"] == "Test Journal"
    
    mock_search.assert_called_once_with("machine learning", 5)


@patch('backend.services.pubmed.pubmed_service.search_articles')
def test_pubmed_search_network_error(mock_search):
    """Test that network errors are handled gracefully."""
    token = _register_and_login()
    
    # Mock network error
    mock_search.side_effect = Exception("Network error")
    
    resp = client.post(
        "/pubmed/search",
        json={"query": "machine learning", "max_results": 5},
        params={"token": token}
    )
    
    # Should return 500 with error message
    assert resp.status_code == 500
    assert "PubMed search failed" in resp.json()["detail"]
    
    # Verify the mock was called
    mock_search.assert_called_once_with("machine learning", 5)


@patch('backend.services.pubmed.pubmed_service.get_article_by_pmid')
def test_import_pubmed_article_new(mock_get_article):
    """Test importing a new PubMed article."""
    token = _register_and_login()
    
    # Mock article data
    mock_get_article.return_value = {
        'pubmed_id': '12345678',
        'title': 'Machine Learning in Healthcare',
        'abstract': 'This study explores the applications of machine learning in healthcare.',
        'authors': 'Johnson, R.; Williams, S.',
        'journal': 'Journal of Medical AI',
        'publication_date': '2023-06-15',
        'doi': '10.1234/jmai.2023.001',
        'keywords': ['machine learning', 'healthcare', 'AI'],
        'url': 'https://pubmed.ncbi.nlm.nih.gov/12345678',
        'citation': 'Johnson, R.; Williams, S. Machine Learning in Healthcare. Journal of Medical AI. 2023-06-15.'
    }
    
    resp = client.post(
        "/pubmed/import",
        json={"pubmed_id": "12345678"},
        params={"token": token}
    )
    
    assert resp.status_code == 200
    data = resp.json()
    assert data["pubmed_id"] == "12345678"
    assert data["title"] == "Machine Learning in Healthcare"
    assert data["authors"] == "Johnson, R.; Williams, S."
    assert data["journal"] == "Journal of Medical AI"
    assert data["year"] == "2023"
    
    mock_get_article.assert_called_once_with("12345678")


@patch('backend.services.pubmed.pubmed_service.get_article_by_pmid')
def test_import_pubmed_article_duplicate(mock_get_article):
    """Test importing a PubMed article that already exists."""
    token = _register_and_login()
    
    # Mock article data
    mock_get_article.return_value = {
        'pubmed_id': '12345678',
        'title': 'Machine Learning in Healthcare',
        'abstract': 'This study explores the applications of machine learning in healthcare.',
        'authors': 'Johnson, R.; Williams, S.',
        'journal': 'Journal of Medical AI',
        'publication_date': '2023-06-15',
        'doi': '10.1234/jmai.2023.001',
        'keywords': ['machine learning', 'healthcare', 'AI'],
        'url': 'https://pubmed.ncbi.nlm.nih.gov/12345678',
        'citation': 'Johnson, R.; Williams, S. Machine Learning in Healthcare. Journal of Medical AI. 2023-06-15.'
    }
    
    # Import first time
    resp1 = client.post(
        "/pubmed/import",
        json={"pubmed_id": "12345678"},
        params={"token": token}
    )
    assert resp1.status_code == 200
    
    # Try to import again - should get 409 conflict
    resp2 = client.post(
        "/pubmed/import",
        json={"pubmed_id": "12345678"},
        params={"token": token}
    )
    assert resp2.status_code == 409
    assert "already exists in your library" in resp2.json()["detail"]


@patch('backend.services.pubmed.pubmed_service.get_article_by_pmid')
def test_import_pubmed_article_link_to_pdf(mock_get_article):
    """Test linking PubMed metadata to existing PDF reference."""
    token = _register_and_login()
    
    # First, upload a PDF reference
    pdf_content = b"test pdf content"
    files = {"pdf": ("test.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"query": "Test PDF"}
    resp = client.post("/references/", params={"token": token}, data=data, files=files)
    assert resp.status_code == 200
    pdf_ref_id = resp.json()["id"]
    
    # Mock PubMed article data
    mock_get_article.return_value = {
        'pubmed_id': '87654321',
        'title': 'Advanced Machine Learning Techniques',
        'abstract': 'This paper presents advanced techniques in machine learning.',
        'authors': 'Brown, M.; Davis, K.',
        'journal': 'AI Research Quarterly',
        'publication_date': '2023-09-10',
        'doi': '10.5678/arq.2023.002',
        'keywords': ['deep learning', 'neural networks'],
        'url': 'https://pubmed.ncbi.nlm.nih.gov/87654321',
        'citation': 'Brown, M.; Davis, K. Advanced Machine Learning Techniques. AI Research Quarterly. 2023-09-10.'
    }
    
    # Link PubMed metadata to the PDF
    resp = client.post(
        "/pubmed/import",
        json={"pubmed_id": "87654321", "link_to_reference_id": pdf_ref_id},
        params={"token": token}
    )
    
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == pdf_ref_id  # Same reference ID
    assert data["pubmed_id"] == "87654321"
    assert data["title"] == "Test PDF"  # Title preserved from PDF upload
    assert data["filename"] == "test.pdf"  # PDF filename preserved
    assert data["abstract"] == "This paper presents advanced techniques in machine learning."
    
    mock_get_article.assert_called_once_with("87654321")


@patch('backend.services.pubmed.pubmed_service.get_article_by_pmid')
def test_get_pubmed_article_by_pmid(mock_get_article):
    """Test getting a specific PubMed article by PMID."""
    token = _register_and_login()
    
    # Mock article data
    mock_get_article.return_value = {
        'pubmed_id': '11111111',
        'title': 'COVID-19 and AI',
        'abstract': 'Analysis of AI applications during the COVID-19 pandemic.',
        'authors': 'Lee, C.; Park, J.',
        'journal': 'Pandemic Studies',
        'publication_date': '2021-12-01',
        'doi': '10.9999/ps.2021.003',
        'keywords': ['COVID-19', 'artificial intelligence'],
        'url': 'https://pubmed.ncbi.nlm.nih.gov/11111111',
        'citation': 'Lee, C.; Park, J. COVID-19 and AI. Pandemic Studies. 2021-12-01.'
    }
    
    resp = client.get(
        "/pubmed/article/11111111",
        params={"token": token}
    )
    
    assert resp.status_code == 200
    data = resp.json()
    assert data["pubmed_id"] == "11111111"
    assert data["title"] == "COVID-19 and AI"
    assert data["authors"] == "Lee, C.; Park, J."
    
    mock_get_article.assert_called_once_with("11111111")


@patch('backend.services.pubmed.pubmed_service.get_article_by_pmid')
def test_get_pubmed_article_not_found(mock_get_article):
    """Test getting a non-existent PubMed article."""
    token = _register_and_login()
    
    # Mock article not found
    mock_get_article.return_value = None
    
    resp = client.get(
        "/pubmed/article/99999999",
        params={"token": token}
    )
    
    assert resp.status_code == 404
    assert "PubMed article not found" in resp.json()["detail"]
    
    mock_get_article.assert_called_once_with("99999999")


def test_pubmed_search_unauthorized():
    """Test PubMed search without authentication."""
    resp = client.post(
        "/pubmed/search",
        json={"query": "machine learning", "max_results": 5}
    )
    
    # Should require authentication
    assert resp.status_code in [401, 422]  # 422 for missing token parameter


@patch('backend.services.pubmed.pubmed_service.get_article_by_pmid')
def test_import_pubmed_article_not_found(mock_get_article):
    """Test importing a non-existent PubMed article."""
    token = _register_and_login()
    
    # Mock article not found
    mock_get_article.return_value = None
    
    resp = client.post(
        "/pubmed/import",
        json={"pubmed_id": "99999999"},
        params={"token": token}
    )
    
    assert resp.status_code == 404
    assert "PubMed article not found" in resp.json()["detail"]
    
    mock_get_article.assert_called_once_with("99999999")


@patch('backend.services.pubmed.pubmed_service.get_article_by_pmid')
def test_import_pubmed_article_link_to_nonexistent_pdf(mock_get_article):
    """Test linking PubMed metadata to non-existent PDF reference."""
    token = _register_and_login()
    
    # Mock PubMed article data
    mock_get_article.return_value = {
        'pubmed_id': '55555555',
        'title': 'Test Article',
        'abstract': 'Test abstract',
        'authors': 'Test Author',
        'journal': 'Test Journal',
        'publication_date': '2023-01-01',
        'doi': '10.1234/test',
        'keywords': [],
        'url': 'https://pubmed.ncbi.nlm.nih.gov/55555555',
        'citation': 'Test citation'
    }
    
    # Try to link to non-existent PDF reference
    resp = client.post(
        "/pubmed/import",
        json={"pubmed_id": "55555555", "link_to_reference_id": 99999},
        params={"token": token}
    )
    
    assert resp.status_code == 404
    assert "PDF reference not found" in resp.json()["detail"]


@patch('backend.services.pubmed.pubmed_service.get_article_by_pmid')
def test_pubmed_article_shared_between_users(mock_get_article):
    """Test that PubMed articles can be shared between users."""
    token1 = _register_and_login()
    token2 = _register_and_login()
    
    # Mock article data
    mock_get_article.return_value = {
        'pubmed_id': '33333333',
        'title': 'Shared Research Article',
        'abstract': 'This article will be shared between users.',
        'authors': 'Researcher, A.; Scientist, B.',
        'journal': 'Collaboration Journal',
        'publication_date': '2023-03-15',
        'doi': '10.1111/cj.2023.001',
        'keywords': ['collaboration', 'research'],
        'url': 'https://pubmed.ncbi.nlm.nih.gov/33333333',
        'citation': 'Researcher, A.; Scientist, B. Shared Research Article. Collaboration Journal. 2023-03-15.'
    }
    
    # User 1 imports the article
    resp1 = client.post(
        "/pubmed/import",
        json={"pubmed_id": "33333333"},
        params={"token": token1}
    )
    assert resp1.status_code == 200
    article_id = resp1.json()["id"]
    
    # User 2 imports the same article (should get access to existing one)
    resp2 = client.post(
        "/pubmed/import",
        json={"pubmed_id": "33333333"},
        params={"token": token2}
    )
    assert resp2.status_code == 200
    assert resp2.json()["id"] == article_id  # Same article ID
    
    # Both users should be able to see the article in their library
    refs1 = client.get("/references/user", params={"token": token1})
    refs2 = client.get("/references/user", params={"token": token2})
    
    assert refs1.status_code == 200
    assert refs2.status_code == 200
    
    # Both should have the article
    user1_articles = [ref for ref in refs1.json() if ref["pubmed_id"] == "33333333"]
    user2_articles = [ref for ref in refs2.json() if ref["pubmed_id"] == "33333333"]
    
    assert len(user1_articles) == 1
    assert len(user2_articles) == 1
    assert user1_articles[0]["id"] == user2_articles[0]["id"]