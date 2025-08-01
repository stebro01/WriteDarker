"""PubMed API service for fetching research articles."""

from typing import List, Dict, Optional
from pymed import PubMed
import logging

logger = logging.getLogger(__name__)


class PubMedService:
    """Service for interacting with PubMed API."""
    
    def __init__(self, tool_name: str = "WriteDarker", email: str = "support@writedarker.com"):
        """Initialize PubMed service with tool identification."""
        self.pubmed = PubMed(tool=tool_name, email=email)
    
    def search_articles(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Search PubMed for articles matching the query.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of article dictionaries with metadata
        """
        try:
            # Search PubMed
            results = self.pubmed.query(query, max_results=max_results)
            
            articles = []
            for article in results:
                try:
                    # Extract article metadata
                    raw_pmid = getattr(article, 'pubmed_id', None)
                    raw_doi = getattr(article, 'doi', '')
                    
                    # Clean up PMID - take only the first one if multiple are concatenated
                    clean_pmid = self._extract_first_id(raw_pmid) if raw_pmid else None
                    
                    # Clean up DOI - take only the first one if multiple are concatenated
                    clean_doi = self._extract_first_doi(raw_doi) if raw_doi else ''
                    
                    article_data = {
                        'pubmed_id': clean_pmid,
                        'title': getattr(article, 'title', ''),
                        'abstract': getattr(article, 'abstract', ''),
                        'authors': self._format_authors(getattr(article, 'authors', [])),
                        'journal': getattr(article, 'journal', ''),
                        'publication_date': self._format_date(getattr(article, 'publication_date', None)),
                        'doi': clean_doi,
                        'keywords': getattr(article, 'keywords', []),
                        'url': f"https://pubmed.ncbi.nlm.nih.gov/{clean_pmid}" if clean_pmid else '',
                        'citation': self._format_citation(article, clean_pmid, clean_doi)
                    }
                    articles.append(article_data)
                except Exception as e:
                    logger.warning(f"Error processing article: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            logger.error(f"Error searching PubMed: {e}")
            raise Exception(f"PubMed search failed: {str(e)}")
    
    def get_article_by_pmid(self, pmid: str) -> Optional[Dict]:
        """
        Get a specific article by PubMed ID.
        
        Args:
            pmid: PubMed ID
            
        Returns:
            Article dictionary or None if not found
        """
        try:
            results = self.search_articles(f"{pmid}[pmid]", max_results=1)
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error fetching article {pmid}: {e}")
            return None
    
    def _format_authors(self, authors) -> str:
        """Format authors list into a string."""
        if not authors:
            return ""
        
        try:
            # Handle different author formats
            if isinstance(authors, list):
                author_names = []
                for author in authors:
                    if hasattr(author, 'lastname') and hasattr(author, 'firstname'):
                        # Format as "Lastname Initials" or "Lastname, Firstname"
                        if hasattr(author, 'initials') and author.initials:
                            name = f"{author.lastname} {author.initials}"
                        else:
                            name = f"{author.lastname}, {author.firstname}"
                        author_names.append(name)
                    elif isinstance(author, str):
                        author_names.append(author)
                    elif isinstance(author, dict):
                        # Handle dictionary format from pymed
                        lastname = author.get('lastname', '')
                        firstname = author.get('firstname', '')
                        initials = author.get('initials', '')
                        
                        if lastname:
                            if initials:
                                name = f"{lastname} {initials}"
                            elif firstname:
                                name = f"{lastname}, {firstname}"
                            else:
                                name = lastname
                            author_names.append(name)
                    else:
                        author_names.append(str(author))
                
                return ", ".join(author_names)
            else:
                return str(authors)
        except Exception as e:
            logger.warning(f"Error formatting authors: {e}")
            return str(authors) if authors else ""
    
    def _format_date(self, date) -> Optional[str]:
        """Format publication date."""
        if not date:
            return None
        
        try:
            # Handle different date formats
            if hasattr(date, 'year'):
                year = date.year
                month = getattr(date, 'month', None)
                day = getattr(date, 'day', None)
                
                if month and day:
                    return f"{year}-{month:02d}-{day:02d}"
                elif month:
                    return f"{year}-{month:02d}"
                else:
                    return str(year)
            else:
                return str(date)
        except Exception as e:
            logger.warning(f"Error formatting date: {e}")
            return str(date) if date else None
    
    def _extract_first_id(self, id_string) -> Optional[str]:
        """Extract the first ID from a potentially concatenated string of IDs."""
        if not id_string:
            return None
        
        # Convert to string and split by whitespace or newlines
        id_str = str(id_string).strip()
        if not id_str:
            return None
        
        # Split by whitespace and take the first valid ID
        parts = id_str.split()
        for part in parts:
            part = part.strip()
            # Check if it looks like a valid PMID (digits only)
            if part.isdigit() and len(part) >= 6:  # PMIDs are typically 6+ digits
                return part
        
        # If no valid numeric ID found, return the first part
        return parts[0] if parts else None
    
    def _extract_first_doi(self, doi_string) -> str:
        """Extract the first DOI from a potentially concatenated string of DOIs."""
        if not doi_string:
            return ""
        
        # Convert to string and split by whitespace or newlines
        doi_str = str(doi_string).strip()
        if not doi_str:
            return ""
        
        # Split by whitespace and take the first valid DOI
        parts = doi_str.split()
        for part in parts:
            part = part.strip()
            # Check if it looks like a valid DOI (contains a dot and slash)
            if '/' in part and '.' in part:
                return part
        
        # If no valid DOI found, return the first part
        return parts[0] if parts else ""
    
    def _format_citation(self, article, clean_pmid=None, clean_doi=None) -> str:
        """Format a citation string for the article."""
        try:
            authors = self._format_authors(getattr(article, 'authors', []))
            title = getattr(article, 'title', '')
            journal = getattr(article, 'journal', '')
            date = self._format_date(getattr(article, 'publication_date', None))
            
            # Create citation in format: Authors. Title. Journal. Date.
            citation_parts = []
            
            if authors:
                citation_parts.append(authors)
            
            if title:
                citation_parts.append(title)
            
            if journal:
                journal_part = journal
                if date:
                    journal_part += f". {date}"
                citation_parts.append(journal_part)
            elif date:
                citation_parts.append(date)
            
            citation = ". ".join(citation_parts) + "." if citation_parts else ""
            
            # Use the cleaned DOI if provided
            if clean_doi:
                citation += f" doi: {clean_doi}"
            
            return citation
            
        except Exception as e:
            logger.warning(f"Error formatting citation: {e}")
            return ""


# Global instance
pubmed_service = PubMedService()