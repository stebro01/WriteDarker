from typing import Optional, List
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
    tag: Optional[str] = None
    filename: Optional[str] = None
    filetype: Optional[str] = None
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
    last_accessed: Optional[datetime] = None
    status: Optional[str] = "active"

    class Config:
        from_attributes = True


class ProjectSummary(ProjectRead):
    document_count: int
    word_count: int
    reference_count: int
    media_count: int
    last_accessed: Optional[datetime] = None
    status: Optional[str] = "active"

    class Config:
        from_attributes = True


class ReferenceCreate(BaseModel):
    project_ids: Optional[list[int]] = None
    query: str


class PubMedSearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 20


class PubMedArticle(BaseModel):
    pubmed_id: Optional[str] = None
    title: str
    abstract: Optional[str] = None
    authors: Optional[str] = None
    journal: Optional[str] = None
    publication_date: Optional[str] = None
    doi: Optional[str] = None
    keywords: Optional[List[str]] = None
    url: Optional[str] = None
    citation: Optional[str] = None


class PubMedSearchResponse(BaseModel):
    articles: List[PubMedArticle]
    total_results: int


class PubMedImportRequest(BaseModel):
    pubmed_id: str
    link_to_reference_id: Optional[int] = None  # Link to existing PDF reference


class ReferenceRead(BaseModel):
    id: int
    title: str
    authors: Optional[str] = None
    journal: Optional[str] = None
    year: Optional[str] = None
    filename: Optional[str] = None
    filetype: Optional[str] = None
    file_hash: Optional[str] = None
    # PubMed fields
    pubmed_id: Optional[str] = None
    doi: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[str] = None
    publication_date: Optional[str] = None
    url: Optional[str] = None
    citation: Optional[str] = None

    class Config:
        from_attributes = True


class ReferenceUpdate(BaseModel):
    title: Optional[str] = None
    authors: Optional[str] = None
    journal: Optional[str] = None
    year: Optional[str] = None
    doi: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[str] = None
    publication_date: Optional[str] = None
    url: Optional[str] = None
    citation: Optional[str] = None


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
