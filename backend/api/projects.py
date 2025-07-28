"""API endpoints for project CRUD operations."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models
from .users import get_db, get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.ProjectRead)
def create_project(project: schemas.ProjectCreate, token: str, db: Session = Depends(get_db)):
    """Create a new project for the current user."""
    user = get_current_user(token, db)
    db_proj = models.Project(
        label=project.label,
        description=project.description,
        author_id=user.id,
        coauthors=project.coauthors,
    )
    db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    return db_proj


@router.get("/{project_id}", response_model=schemas.ProjectRead)
def read_project(project_id: int, token: str, db: Session = Depends(get_db)):
    """Return a single project if owned by the current user."""
    user = get_current_user(token, db)
    proj = db.query(models.Project).filter(models.Project.id == project_id, models.Project.author_id == user.id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


@router.put("/{project_id}", response_model=schemas.ProjectRead)
def update_project(project_id: int, update: schemas.ProjectUpdate, token: str, db: Session = Depends(get_db)):
    """Update a project owned by the current user."""
    user = get_current_user(token, db)
    proj = db.query(models.Project).filter(models.Project.id == project_id, models.Project.author_id == user.id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    if update.label is not None:
        proj.label = update.label
    if update.description is not None:
        proj.description = update.description
    if update.coauthors is not None:
        proj.coauthors = update.coauthors
    db.commit()
    db.refresh(proj)
    return proj


@router.delete("/{project_id}")
def delete_project(project_id: int, token: str, db: Session = Depends(get_db)):
    """Delete a project owned by the current user."""
    user = get_current_user(token, db)
    proj = db.query(models.Project).filter(models.Project.id == project_id, models.Project.author_id == user.id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(proj)
    db.commit()
    return {"message": "deleted"}
