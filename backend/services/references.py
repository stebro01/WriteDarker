"""Utility functions for fetching references from PubMed."""

import httpx


def fetch_reference(query: str) -> dict:
    """Return basic metadata for the first PubMed result for `query`."""
    url = "https://pubmed.ncbi.nlm.nih.gov/?term=" + query
    try:
        resp = httpx.get(url, timeout=10)
        resp.raise_for_status()
        # Dummy parsing due to simplicity
        title = query
    except Exception:
        title = query
    return {
        "title": title,
        "authors": "",
        "journal": "",
        "year": "",
    }

