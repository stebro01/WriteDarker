from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    password: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class DocumentBase(BaseModel):
    text: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    project_id: Optional[int] = None
    position: Optional[int] = None

class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(DocumentBase):
    pass

class DocumentRead(DocumentBase):
    id: int

    class Config:
        from_attributes = True


class DocumentRevisionRead(BaseModel):
    id: int
    document_id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    label: str
    description: Optional[str] = None
    coauthors: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None
    coauthors: Optional[str] = None


class ProjectRead(ProjectBase):
    id: int

    class Config:
        from_attributes = True


class ReferenceCreate(BaseModel):
    project_ids: Optional[list[int]] = None
    query: str


class ReferenceRead(BaseModel):
    id: int
    title: str
    authors: str
    journal: str
    year: str
    filename: Optional[str] = None
    filetype: Optional[str] = None

    class Config:
        from_attributes = True


class SettingCreate(BaseModel):
    key: str
    value: str
    user_based: bool = True


class SettingRead(BaseModel):
    id: int
    key: str
    value: str
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
