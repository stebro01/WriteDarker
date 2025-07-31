"""API endpoints for PubMed integration."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models
from ..services.pubmed import pubmed_service
from .users import get_db, get_current_user

router = APIRouter()


@router.post("/search", response_model=schemas.PubMedSearchResponse)
def search_pubmed(
    search_request: schemas.PubMedSearchRequest,
    token: str,
    db: Session = Depends(get_db)
):
    """Search PubMed for articles."""
    user = get_current_user(token, db)
    
    try:
        articles_data = pubmed_service.search_articles(
            search_request.query, 
            search_request.max_results
        )
        
        # Convert to PubMedArticle schemas
        articles = []
        for article_data in articles_data:
            article = schemas.PubMedArticle(
                pubmed_id=article_data.get('pubmed_id'),
                title=article_data.get('title', ''),
                abstract=article_data.get('abstract'),
                authors=article_data.get('authors'),
                journal=article_data.get('journal'),
                publication_date=article_data.get('publication_date'),
                doi=article_data.get('doi'),
                keywords=article_data.get('keywords', []),
                url=article_data.get('url'),
                citation=article_data.get('citation')
            )
            articles.append(article)
        
        return schemas.PubMedSearchResponse(
            articles=articles,
            total_results=len(articles)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PubMed search failed: {str(e)}")


@router.post("/import", response_model=schemas.ReferenceRead)
def import_pubmed_article(
    import_request: schemas.PubMedImportRequest,
    token: str,
    db: Session = Depends(get_db)
):
    """Import a PubMed article as a reference."""
    user = get_current_user(token, db)
    
    try:
        # Get article data from PubMed
        article_data = pubmed_service.get_article_by_pmid(import_request.pubmed_id)
        if not article_data:
            raise HTTPException(status_code=404, detail="PubMed article not found")
        
        # Handle linking to existing PDF reference first
        if import_request.link_to_reference_id:
            existing_pdf_ref = db.query(models.Reference).join(models.Reference.shared_with).filter(
                models.Reference.id == import_request.link_to_reference_id,
                models.User.id == user.id
            ).first()
            
            if not existing_pdf_ref:
                raise HTTPException(status_code=404, detail="PDF reference not found or not accessible")
            
            # Update existing PDF reference with PubMed metadata
            existing_pdf_ref.pubmed_id = article_data.get('pubmed_id')
            existing_pdf_ref.doi = article_data.get('doi')
            existing_pdf_ref.abstract = article_data.get('abstract')
            existing_pdf_ref.keywords = ', '.join(article_data.get('keywords', [])) if article_data.get('keywords') else None
            existing_pdf_ref.publication_date = article_data.get('publication_date')
            existing_pdf_ref.url = article_data.get('url')
            existing_pdf_ref.citation = article_data.get('citation')
            
            # Update basic fields if they're empty
            if not existing_pdf_ref.title or existing_pdf_ref.title == existing_pdf_ref.filename:
                existing_pdf_ref.title = article_data.get('title', existing_pdf_ref.title)
            if not existing_pdf_ref.authors:
                existing_pdf_ref.authors = article_data.get('authors')
            if not existing_pdf_ref.journal:
                existing_pdf_ref.journal = article_data.get('journal')
            if not existing_pdf_ref.year:
                # Extract year from publication_date
                pub_date = article_data.get('publication_date')
                if pub_date:
                    year = pub_date.split('-')[0] if '-' in pub_date else pub_date
                    existing_pdf_ref.year = year
            
            db.commit()
            db.refresh(existing_pdf_ref)
            return existing_pdf_ref
        
        # Check if we already have this article (only if not linking to existing PDF)
        existing_ref = db.query(models.Reference).filter(
            models.Reference.pubmed_id == import_request.pubmed_id
        ).first()
        
        if existing_ref:
            # Check if user already has access
            user_has_access = db.query(models.Reference).join(models.Reference.shared_with).filter(
                models.Reference.id == existing_ref.id,
                models.User.id == user.id
            ).first()
            
            if user_has_access:
                raise HTTPException(status_code=409, detail="Article already exists in your library")
            else:
                # Give user access to existing article
                existing_ref.shared_with.append(user)
                db.commit()
                db.refresh(existing_ref)
                return existing_ref
        
        # Create new reference from PubMed data
        new_ref = models.Reference(
            title=article_data.get('title', ''),
            authors=article_data.get('authors'),
            journal=article_data.get('journal'),
            year=article_data.get('publication_date', '').split('-')[0] if article_data.get('publication_date') else None,
            pubmed_id=article_data.get('pubmed_id'),
            doi=article_data.get('doi'),
            abstract=article_data.get('abstract'),
            keywords=', '.join(article_data.get('keywords', [])) if article_data.get('keywords') else None,
            publication_date=article_data.get('publication_date'),
            url=article_data.get('url'),
            citation=article_data.get('citation')
        )
        
        # Add user access
        new_ref.shared_with.append(user)
        
        db.add(new_ref)
        db.commit()
        db.refresh(new_ref)
        
        return new_ref
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@router.get("/article/{pmid}", response_model=schemas.PubMedArticle)
def get_pubmed_article(pmid: str, token: str, db: Session = Depends(get_db)):
    """Get a specific PubMed article by PMID."""
    user = get_current_user(token, db)
    
    try:
        article_data = pubmed_service.get_article_by_pmid(pmid)
        if not article_data:
            raise HTTPException(status_code=404, detail="PubMed article not found")
        
        return schemas.PubMedArticle(
            pubmed_id=article_data.get('pubmed_id'),
            title=article_data.get('title', ''),
            abstract=article_data.get('abstract'),
            authors=article_data.get('authors'),
            journal=article_data.get('journal'),
            publication_date=article_data.get('publication_date'),
            doi=article_data.get('doi'),
            keywords=article_data.get('keywords', []),
            url=article_data.get('url'),
            citation=article_data.get('citation')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch article: {str(e)}")