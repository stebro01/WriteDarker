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
    db_ref = models.Reference(
        owner_id=user.id,
        pdf=pdf_bytes,
        filename=filename,
        filetype=filetype,
        **data,
    )
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
    """List all references owned by the current user with optional search and sorting."""
    user = get_current_user(token, db)
    q = db.query(models.Reference).filter(models.Reference.owner_id == user.id)
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
    """Return a reference belonging to the current user."""
    user = get_current_user(token, db)
    ref = (
        db.query(models.Reference)
        .filter(models.Reference.id == ref_id, models.Reference.owner_id == user.id)
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
        .join(models.Reference.projects)
        .filter(models.Project.id == project_id, models.Project.author_id == user.id)
        .all()
    )
    return refs




@router.delete("/{ref_id}")
def delete_reference(ref_id: int, token: str, db: Session = Depends(get_db)):
    """Delete a reference owned by the current user."""
    user = get_current_user(token, db)
    ref = (
        db.query(models.Reference)
        .filter(models.Reference.id == ref_id, models.Reference.owner_id == user.id)
        .first()
    )
    if not ref:
        raise HTTPException(status_code=404, detail="Reference not found")
    db.delete(ref)
    db.commit()
    return {"message": "deleted"}

