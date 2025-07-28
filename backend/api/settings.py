"""API endpoints for user and global settings."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models
from .users import get_db, get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.SettingRead)
def set_setting(setting: schemas.SettingCreate, token: str, db: Session = Depends(get_db)):
    """Create or update a setting for the current user."""
    user = get_current_user(token, db) if setting.user_based else None
    query = db.query(models.Setting).filter(models.Setting.key == setting.key)
    if user:
        query = query.filter(models.Setting.user_id == user.id)
    else:
        query = query.filter(models.Setting.user_id.is_(None))
    obj = query.first()
    if obj:
        obj.value = setting.value
    else:
        obj = models.Setting(key=setting.key, value=setting.value, user_id=user.id if user else None)
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{key}", response_model=schemas.SettingRead)
def get_setting(key: str, token: str = "", db: Session = Depends(get_db)):
    """Retrieve a setting. User-specific value overrides global."""
    user = None
    if token:
        try:
            user = get_current_user(token, db)
        except HTTPException:
            user = None
    if user:
        obj = db.query(models.Setting).filter(models.Setting.key == key, models.Setting.user_id == user.id).first()
        if obj:
            return obj
    obj = db.query(models.Setting).filter(models.Setting.key == key, models.Setting.user_id.is_(None)).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Setting not found")
    return obj

