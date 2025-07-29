"""API endpoints for managing references."""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models
from ..services import references as ref_service
from .users import get_db, get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.ReferenceRead)
def add_reference(
    token: str,
    project_id: int = Form(...),
    query: str = Form(...),
    pdf: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    """Add a reference to a project."""
    user = get_current_user(token, db)
    proj = db.query(models.Project).filter(models.Project.id == project_id, models.Project.author_id == user.id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    data = ref_service.fetch_reference(query)
    pdf_bytes = pdf.file.read() if pdf else None
    db_ref = models.Reference(project_id=proj.id, pdf=pdf_bytes, **data)
    db.add(db_ref)
    db.commit()
    db.refresh(db_ref)
    return db_ref


@router.get("/{ref_id}", response_model=schemas.ReferenceRead)
def read_reference(ref_id: int, token: str, db: Session = Depends(get_db)):
    """Return a reference belonging to the current user."""
    user = get_current_user(token, db)
    ref = (
        db.query(models.Reference)
        .join(models.Project)
        .filter(models.Reference.id == ref_id, models.Project.author_id == user.id)
        .first()
    )
    if not ref:
        raise HTTPException(status_code=404, detail="Reference not found")
    return ref


@router.get("/project/{project_id}", response_model=List[schemas.ReferenceRead])
def list_references(project_id: int, token: str, db: Session = Depends(get_db)):
    """List references for a project."""
    user = get_current_user(token, db)
    refs = (
        db.query(models.Reference)
        .join(models.Project)
        .filter(models.Project.id == project_id, models.Project.author_id == user.id)
        .all()
    )
    return refs

