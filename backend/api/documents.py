"""API endpoints for document management."""

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from PyPDF2 import PdfReader
import io

from .. import schemas, models
from ..services import auth
from .users import get_db, get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.DocumentRead)
def create_document(
    token: str,
    text: Optional[str] = None,
    pdf: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    label: Optional[str] = None,
    description: Optional[str] = None,
    notes: Optional[str] = None,
    project_id: Optional[int] = None,
    position: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Create a new document owned by the current user."""

    user = get_current_user(token, db)

    pdf_bytes = None
    extracted_text = text
    if pdf is not None:
        content = pdf.file.read()
        pdf_bytes = content
        try:
            reader = PdfReader(io.BytesIO(content))
            extracted_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            pass

    image_bytes = None
    if image is not None:
        image_bytes = image.file.read()

    doc = models.Document(
        text=extracted_text,
        pdf=pdf_bytes,
        image=image_bytes,
        label=label,
        description=description,
        notes=notes,
        project_id=project_id,
        position=position or 0,
        creator_id=user.id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.get("/{doc_id}", response_model=schemas.DocumentRead)
def read_document(doc_id: int, token: str, db: Session = Depends(get_db)):
    """Return a single document owned by the user."""

    user = get_current_user(token, db)
    doc = db.query(models.Document).filter(models.Document.id == doc_id, models.Document.creator_id == user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.put("/{doc_id}", response_model=schemas.DocumentRead)
def update_document(
    doc_id: int,
    update: schemas.DocumentUpdate,
    token: str,
    db: Session = Depends(get_db),
):
    """Update an existing document."""
    user = get_current_user(token, db)
    doc = (
        db.query(models.Document)
        .filter(models.Document.id == doc_id, models.Document.creator_id == user.id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if update.text is not None:
        doc.text = update.text
    if update.label is not None:
        doc.label = update.label
    if update.description is not None:
        doc.description = update.description
    if update.notes is not None:
        doc.notes = update.notes
    if update.project_id is not None:
        doc.project_id = update.project_id
    if update.position is not None:
        doc.position = update.position
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/{doc_id}")
def delete_document(doc_id: int, token: str, db: Session = Depends(get_db)):
    """Delete a document owned by the current user."""

    user = get_current_user(token, db)
    doc = db.query(models.Document).filter(models.Document.id == doc_id, models.Document.creator_id == user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return {"message": "deleted"}


@router.get("/project/{project_id}", response_model=List[schemas.DocumentRead])
def list_project_documents(project_id: int, token: str, db: Session = Depends(get_db)):
    """List documents belonging to a project ordered by position."""
    user = get_current_user(token, db)
    docs = (
        db.query(models.Document)
        .filter(
            models.Document.project_id == project_id,
            models.Document.creator_id == user.id,
        )
        .order_by(models.Document.position)
        .all()
    )
    return docs
