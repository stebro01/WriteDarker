"""Utility functions for fetching references from PubMed."""

from xml.etree import ElementTree

import httpx


def _parse_pubmed_xml(xml: str) -> dict:
    """Parse minimal fields from an efetch PubMed XML response."""
    tree = ElementTree.fromstring(xml)

    article = tree.find(".//PubmedArticle")
    if article is None:
        return {}

    title = article.findtext(".//ArticleTitle", default="")
    year = (
        article.findtext(".//PubDate/Year")
        or article.findtext(".//PubDate/MedlineDate", default="")[:4]
    )
    journal = article.findtext(".//ISOAbbreviation", default="")

    authors = []
    for author in article.findall(".//Author"):
        last = author.findtext("LastName")
        initials = author.findtext("Initials")
        if last and initials:
            authors.append(f"{last} {initials}")
    authors_str = ", ".join(authors)

    return {
        "title": title,
        "authors": authors_str,
        "journal": journal,
        "year": year,
    }


def fetch_reference(query: str) -> dict:
    """Return basic metadata for a PubMed ID or search term."""
    default_data = {
        "title": query,
        "authors": "",
        "journal": "",
        "year": "",
    }

    if query.isdigit():
        url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed"
            f"&id={query}&retmode=xml"
        )
        try:
            resp = httpx.get(url, timeout=10)
            resp.raise_for_status()
        except httpx.HTTPError:
            return default_data
        data = _parse_pubmed_xml(resp.text)
        if data:
            return data

    # fallback to original behaviour for arbitrary queries
    return default_data

