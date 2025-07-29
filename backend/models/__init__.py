"""Database models for the application."""

from sqlalchemy import (
    Column,
    Integer,
    String,
    LargeBinary,
    Text,
    ForeignKey,
    DateTime,
)
from datetime import datetime
from sqlalchemy.orm import relationship

from ..db import Base

__all__ = [
    "User",
    "Document",
    "DocumentRevision",
    "Project",
    "Reference",
    "Setting",
]

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)

    documents = relationship("Document", back_populates="owner")

class Document(Base):
    """Represents an uploaded or generated document."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    pdf = Column(LargeBinary)
    image = Column(LargeBinary)
    label = Column(String)
    description = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    notes = Column(String)
    position = Column(Integer, default=0)

    owner = relationship("User", back_populates="documents")
    project = relationship("Project", back_populates="documents")
    revisions = relationship("DocumentRevision", back_populates="document", cascade="all, delete-orphan")


class Project(Base):
    """A collection of documents with associated metadata."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)
    description = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    coauthors = Column(String)

    author = relationship("User")
    documents = relationship("Document", back_populates="project")
    references = relationship("Reference", back_populates="project")


class Reference(Base):
    """Bibliographic reference fetched from an external source."""

    __tablename__ = "references"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    authors = Column(String)
    journal = Column(String)
    year = Column(String)
    pdf = Column(LargeBinary)
    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="references")


class Setting(Base):
    """User or global configuration setting."""

    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User")


class DocumentRevision(Base):
    """Historical record of document text changes."""

    __tablename__ = "document_revisions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="revisions")
