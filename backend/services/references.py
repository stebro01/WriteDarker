"""Utility functions for fetching references from PubMed."""

from xml.etree import ElementTree

import httpx


def _parse_pubmed_xml(xml: str) -> dict:
    """Parse fields from an efetch PubMed XML response."""
    tree = ElementTree.fromstring(xml)

    article = tree.find(".//PubmedArticle")
    if article is None:
        return {}

    # Get PMID from the MedlineCitation element (more reliable)
    medline_citation = article.find(".//MedlineCitation")
    pubmed_id = None
    if medline_citation is not None:
        pmid_elem = medline_citation.find("PMID")
        if pmid_elem is not None:
            pubmed_id = pmid_elem.text
    
    # Basic article info - ensure we're looking within this specific article
    title = article.findtext(".//ArticleTitle", default="")
    
    # Abstract - handle multiple AbstractText elements
    abstract_texts = []
    for abstract_text in article.findall(".//Abstract/AbstractText"):
        if abstract_text.text:
            abstract_texts.append(abstract_text.text)
    abstract = " ".join(abstract_texts) if abstract_texts else ""
    
    journal = article.findtext(".//ISOAbbreviation", default="")
    
    # Publication date
    pub_date_elem = article.find(".//PubDate")
    pub_year = None
    pub_month = "01"
    pub_day = "01"
    
    if pub_date_elem is not None:
        pub_year = pub_date_elem.findtext("Year")
        pub_month = pub_date_elem.findtext("Month", default="01")
        pub_day = pub_date_elem.findtext("Day", default="01")
        
        if not pub_year:
            medline_date = pub_date_elem.findtext("MedlineDate", default="")
            if medline_date:
                pub_year = medline_date[:4]
        
    publication_date = f"{pub_year}-{pub_month.zfill(2)}-{pub_day.zfill(2)}" if pub_year else None

    # Authors - ensure we're only getting authors from this article
    authors = []
    author_list = article.find(".//AuthorList")
    if author_list is not None:
        for author in author_list.findall("Author"):
            last = author.findtext("LastName")
            initials = author.findtext("Initials")
            if last and initials:
                authors.append(f"{last} {initials}")
    authors_str = ", ".join(authors)

    # DOI and other identifiers - only from this article's PubmedData
    doi = None
    url = None
    pubmed_data = article.find(".//PubmedData")
    if pubmed_data is not None:
        article_id_list = pubmed_data.find("ArticleIdList")
        if article_id_list is not None:
            for id_elem in article_id_list.findall("ArticleId"):
                id_type = id_elem.get("IdType", "")
                if id_type.lower() == "doi":
                    doi = id_elem.text
                elif id_type.lower() == "pubmed" and not url:
                    url = f"https://pubmed.ncbi.nlm.nih.gov/{id_elem.text}/"

    # If no URL from ArticleIdList, use the PMID we found
    if not url and pubmed_id:
        url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"

    # Keywords - only from this article
    keywords = []
    keyword_list = article.find(".//KeywordList")
    if keyword_list is not None:
        for keyword in keyword_list.findall("Keyword"):
            if keyword.text:
                keywords.append(keyword.text)

    # Build citation
    citation_parts = []
    if authors_str:
        citation_parts.append(authors_str)
    if title:
        citation_parts.append(title)
    if journal and pub_year:
        citation_parts.append(f"{journal}. {pub_year}")
    elif journal:
        citation_parts.append(journal)
    elif pub_year:
        citation_parts.append(pub_year)
    
    citation = ". ".join(citation_parts)
    if doi:
        citation += f". doi: {doi}"

    return {
        "pubmed_id": pubmed_id,
        "title": title,
        "abstract": abstract,
        "authors": authors_str,
        "journal": journal,
        "publication_date": publication_date,
        "year": pub_year,
        "doi": doi,
        "keywords": keywords,
        "url": url,
        "citation": citation
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

