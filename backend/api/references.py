"""API endpoints for managing references."""

import hashlib
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models
from ..services import references as ref_service
from .users import get_db, get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.ReferenceRead)
def add_reference(
    token: str,
    query: str = Form(...),
    project_ids: list[int] | None = Form(None),
    pdf: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    """Add a reference to a project."""
    user = get_current_user(token, db)
    data = ref_service.fetch_reference(query)
    
    pdf_bytes = pdf.file.read() if pdf else None
    filename = pdf.filename if pdf else None
    filetype = pdf.content_type if pdf else None
    file_hash = None
    
    # Calculate file hash if a file is uploaded
    if pdf_bytes:
        file_hash = hashlib.sha256(pdf_bytes).hexdigest()
        
        # Check if a reference with this hash already exists
        existing_ref = db.query(models.Reference).filter(
            models.Reference.file_hash == file_hash
        ).first()
        
        if existing_ref:
            # Check if the user already has access to this reference
            user_has_access = user in existing_ref.shared_with
            
            if user_has_access:
                raise HTTPException(
                    status_code=409, 
                    detail=f"File already exists in your library: '{existing_ref.filename}'"
                )
            else:
                # Share the existing reference with this user
                existing_ref.shared_with.append(user)
                
                # Update metadata if the user provided different information
                # This allows users to have their own "view" of the same file
                if filename and filename != existing_ref.filename:
                    # Keep the original filename but could be extended to support per-user metadata
                    pass
                
                db.commit()
                db.refresh(existing_ref)
                
                # Return success - user now has access to this reference
                return existing_ref
    
    db_ref = models.Reference(
        pdf=pdf_bytes,
        filename=filename,
        filetype=filetype,
        file_hash=file_hash,
        **data,
    )
    
    # Add the creating user to the reference_to_owner table
    db_ref.shared_with.append(user)
    
    if project_ids:
        projects = (
            db.query(models.Project)
            .filter(models.Project.id.in_(project_ids), models.Project.author_id == user.id)
            .all()
        )
        if len(projects) != len(set(project_ids)):
            raise HTTPException(status_code=404, detail="Project not found")
        db_ref.projects.extend(projects)
    
    db.add(db_ref)
    db.commit()
    db.refresh(db_ref)
    return db_ref


@router.get("/user", response_model=List[schemas.ReferenceRead])
def list_user_references(
    token: str,
    search: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db),
):
    """List all references shared with the current user with optional search and sorting."""
    user = get_current_user(token, db)
    
    # Get references shared with user via reference_to_owner table
    q = db.query(models.Reference).join(models.Reference.shared_with).filter(
        models.User.id == user.id
    )
    
    if search:
        like = f"%{search}%"
        q = q.filter(
            models.Reference.title.ilike(like)
            | models.Reference.authors.ilike(like)
            | models.Reference.journal.ilike(like)
            | models.Reference.year.ilike(like)
        )
    if sort:
        desc = False
        if sort.startswith("-"):
            desc = True
            sort_field = sort[1:]
        else:
            sort_field = sort
        column = getattr(models.Reference, sort_field, None)
        if column is not None:
            q = q.order_by(column.desc() if desc else column)
    return q.all()





@router.get("/{ref_id}", response_model=schemas.ReferenceRead)
def read_reference(ref_id: int, token: str, db: Session = Depends(get_db)):
    """Return a reference shared with the current user."""
    user = get_current_user(token, db)
    
    # Check if reference is shared with the user
    ref = db.query(models.Reference).join(models.Reference.shared_with).filter(
        models.Reference.id == ref_id,
        models.User.id == user.id
    ).first()
    
    if not ref:
        raise HTTPException(status_code=404, detail="Reference not found")
    return ref


@router.put("/{ref_id}", response_model=schemas.ReferenceRead)
def update_reference(
    ref_id: int,
    update: schemas.ReferenceUpdate,
    token: str,
    db: Session = Depends(get_db),
):
    """Update a reference's metadata."""
    user = get_current_user(token, db)
    
    # Get the reference - must be one the user has access to
    ref = db.query(models.Reference).join(
        models.Reference.shared_with
    ).filter(
        models.Reference.id == ref_id,
        models.User.id == user.id
    ).first()
    
    if not ref:
        raise HTTPException(status_code=404, detail="Reference not found")
    
    # Update only the provided fields
    if update.title is not None:
        ref.title = update.title
    if update.authors is not None:
        ref.authors = update.authors
    if update.journal is not None:
        ref.journal = update.journal
    if update.year is not None:
        ref.year = update.year
    if update.doi is not None:
        ref.doi = update.doi
    if update.abstract is not None:
        ref.abstract = update.abstract
    if update.keywords is not None:
        ref.keywords = update.keywords
    if update.publication_date is not None:
        ref.publication_date = update.publication_date
    if update.url is not None:
        ref.url = update.url
    if update.citation is not None:
        ref.citation = update.citation
    
    db.commit()
    db.refresh(ref)
    return ref


@router.get("/project/{project_id}", response_model=List[schemas.ReferenceRead])
def list_references(project_id: int, token: str, db: Session = Depends(get_db)):
    """List references for a project."""
    user = get_current_user(token, db)
    refs = (
        db.query(models.Reference)
        .join(models.Reference.projects)
        .filter(models.Project.id == project_id, models.Project.author_id == user.id)
        .all()
    )
    return refs




@router.get("/{ref_id}/file")
def get_reference_file(ref_id: int, token: str, db: Session = Depends(get_db)):
    """Return the file content for a reference that the user has access to."""
    user = get_current_user(token, db)
    
    # Check if reference is shared with the user
    ref = db.query(models.Reference).join(models.Reference.shared_with).filter(
        models.Reference.id == ref_id,
        models.User.id == user.id
    ).first()
    
    if not ref:
        raise HTTPException(status_code=404, detail="Reference not found")
    
    if not ref.pdf:
        raise HTTPException(status_code=404, detail="No file content available")
    
    # Return the file content with appropriate headers
    media_type = ref.filetype or "application/octet-stream"
    filename = ref.filename or f"reference_{ref_id}"
    
    return Response(
        content=ref.pdf,
        media_type=media_type,
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )


@router.delete("/{ref_id}")
def delete_reference(ref_id: int, token: str, db: Session = Depends(get_db)):
    """Remove access to a reference for the current user, or delete it entirely if no users have access."""
    user = get_current_user(token, db)
    
    # Find the reference that the user has access to
    ref = db.query(models.Reference).join(models.Reference.shared_with).filter(
        models.Reference.id == ref_id,
        models.User.id == user.id
    ).first()
    
    if not ref:
        raise HTTPException(status_code=404, detail="Reference not found")
    
    # Remove the user from the reference_to_owner table
    ref.shared_with.remove(user)
    
    # If no users have access to this reference anymore, delete it entirely
    if not ref.shared_with:
        db.delete(ref)
    
    db.commit()
    return {"message": "deleted"}

