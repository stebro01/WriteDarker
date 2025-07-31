"""API endpoints for document management."""

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status, Form
from fastapi.responses import Response
from diff_match_patch import diff_match_patch
from sqlalchemy.orm import Session
from typing import Optional, List
from PyPDF2 import PdfReader
import io
import os

from .. import schemas, models
from ..services import auth
from .users import get_db, get_current_user

router = APIRouter()


def _add_revision(db: Session, doc: models.Document):
    """Store the current text of a document as a revision and enforce history limit."""
    rev = models.DocumentRevision(document_id=doc.id, text=doc.text)
    db.add(rev)
    db.commit()
    limit = int(os.getenv("DOC_HISTORY_LIMIT", "20"))
    q = (
        db.query(models.DocumentRevision)
        .filter(models.DocumentRevision.document_id == doc.id)
        .order_by(models.DocumentRevision.created_at.desc())
    )
    revisions = q.all()
    if len(revisions) > limit:
        for r in revisions[limit:]:
            db.delete(r)
        db.commit()


@router.post("/", response_model=schemas.DocumentRead)
def create_document(
    token: str,
    text: Optional[str] = Form(None),
    pdf: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    label: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    tag: Optional[str] = Form(None),
    filename: Optional[str] = Form(None),
    filetype: Optional[str] = Form(None),
    project_id: Optional[int] = Form(None),
    position: Optional[int] = Form(None),
    db: Session = Depends(get_db),
):
    """Create a new document owned by the current user."""

    user = get_current_user(token, db)

    pdf_bytes = None
    extracted_text = text
    if pdf is not None:
        content = pdf.file.read()
        pdf_bytes = content
        filename = filename or pdf.filename
        filetype = filetype or pdf.content_type
        try:
            reader = PdfReader(io.BytesIO(content))
            extracted_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            pass

    image_bytes = None
    if image is not None:
        image_bytes = image.file.read()
        filename = filename or image.filename
        filetype = filetype or image.content_type

    doc = models.Document(
        text=extracted_text,
        pdf=pdf_bytes,
        image=image_bytes,
        label=label,
        description=description,
        notes=notes,
        tag=tag,
        filename=filename,
        filetype=filetype,
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
    if update.text is not None and update.text != doc.text:
        _add_revision(db, doc)
        doc.text = update.text
    if update.label is not None:
        doc.label = update.label
    if update.description is not None:
        doc.description = update.description
    if update.notes is not None:
        doc.notes = update.notes
    if update.tag is not None:
        doc.tag = update.tag
    if update.filename is not None:
        doc.filename = update.filename
    if update.filetype is not None:
        doc.filetype = update.filetype
    if update.project_id is not None:
        doc.project_id = update.project_id
    if update.position is not None:
        doc.position = update.position
    db.commit()
    db.refresh(doc)
    return doc


@router.patch("/{doc_id}", response_model=schemas.DocumentRead)
def patch_document(doc_id: int, patch: str, token: str, db: Session = Depends(get_db)):
    """Apply a diff/patch string to a document."""
    user = get_current_user(token, db)
    doc = (
        db.query(models.Document)
        .filter(models.Document.id == doc_id, models.Document.creator_id == user.id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    dmp = diff_match_patch()
    patches = dmp.patch_fromText(patch)
    new_text, _ = dmp.patch_apply(patches, doc.text or "")
    if new_text != doc.text:
        _add_revision(db, doc)
        doc.text = new_text
        db.commit()
        db.refresh(doc)
    return doc


@router.post("/{doc_id}/pdf", response_model=schemas.DocumentRead)
def upload_pdf(doc_id: int, token: str, pdf: UploadFile = File(...), db: Session = Depends(get_db)):
    """Attach or replace a PDF for a document."""
    user = get_current_user(token, db)
    doc = db.query(models.Document).filter(models.Document.id == doc_id, models.Document.creator_id == user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc.pdf = pdf.file.read()
    doc.filename = pdf.filename
    doc.filetype = pdf.content_type
    db.commit()
    db.refresh(doc)
    return doc


@router.post("/{doc_id}/image", response_model=schemas.DocumentRead)
def upload_image(doc_id: int, token: str, image: UploadFile = File(...), db: Session = Depends(get_db)):
    """Attach or replace an image for a document."""
    user = get_current_user(token, db)
    doc = db.query(models.Document).filter(models.Document.id == doc_id, models.Document.creator_id == user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc.image = image.file.read()
    doc.filename = image.filename
    doc.filetype = image.content_type
    db.commit()
    db.refresh(doc)
    return doc


@router.get("/{doc_id}/file")
def get_document_file(doc_id: int, token: str, db: Session = Depends(get_db)):
    """Return binary file content for a document."""
    user = get_current_user(token, db)
    doc = (
        db.query(models.Document)
        .filter(models.Document.id == doc_id, models.Document.creator_id == user.id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    content = doc.pdf or doc.image
    if not content:
        raise HTTPException(status_code=404, detail="No file content available")
    media_type = doc.filetype or ("application/pdf" if doc.pdf else "application/octet-stream")
    filename = doc.filename or f"document_{doc_id}"
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f"inline; filename={filename}"},
    )


@router.get("/{doc_id}/revisions", response_model=List[schemas.DocumentRevisionRead])
def list_revisions(doc_id: int, token: str, db: Session = Depends(get_db)):
    """Return revision history for a document."""
    user = get_current_user(token, db)
    doc = (
        db.query(models.Document)
        .filter(models.Document.id == doc_id, models.Document.creator_id == user.id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    revs = (
        db.query(models.DocumentRevision)
        .filter(models.DocumentRevision.document_id == doc_id)
        .order_by(models.DocumentRevision.created_at)
        .all()
    )
    return revs


@router.post("/{doc_id}/restore/{rev_id}", response_model=schemas.DocumentRead)
def restore_revision(doc_id: int, rev_id: int, token: str, db: Session = Depends(get_db)):
    """Restore a document to a previous revision."""
    user = get_current_user(token, db)
    doc = (
        db.query(models.Document)
        .filter(models.Document.id == doc_id, models.Document.creator_id == user.id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    rev = (
        db.query(models.DocumentRevision)
        .filter(models.DocumentRevision.id == rev_id, models.DocumentRevision.document_id == doc_id)
        .first()
    )
    if not rev:
        raise HTTPException(status_code=404, detail="Revision not found")
    if rev.text != doc.text:
        _add_revision(db, doc)
        doc.text = rev.text
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
