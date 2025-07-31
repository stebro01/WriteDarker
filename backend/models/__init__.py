"""Database models for the application."""

from sqlalchemy import (
    Column,
    Integer,
    String,
    LargeBinary,
    Text,
    ForeignKey,
    DateTime,
    Table,
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

# Association table between projects and references for many-to-many relation
project_reference_link = Table(
    "project_references",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("reference_id", Integer, ForeignKey("references.id"), primary_key=True),
)

# Association table between references and owners for many-to-many relation
reference_owner_link = Table(
    "reference_to_owner",
    Base.metadata,
    Column("reference_id", Integer, ForeignKey("references.id"), primary_key=True),
    Column("owner_id", Integer, ForeignKey("users.id"), primary_key=True),
)

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
    shared_references = relationship(
        "Reference",
        secondary=reference_owner_link,
        back_populates="shared_with",
    )

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
    references = relationship(
        "Reference",
        secondary=project_reference_link,
        back_populates="projects",
    )


class Reference(Base):
    """Bibliographic reference fetched from an external source."""

    __tablename__ = "references"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    authors = Column(String)
    journal = Column(String)
    year = Column(String)
    pdf = Column(LargeBinary)
    filename = Column(String)
    filetype = Column(String)
    file_hash = Column(String, index=True)  # SHA-256 hash of the file content
    
    # PubMed-specific fields
    pubmed_id = Column(String, index=True)  # PubMed ID (PMID)
    doi = Column(String)  # Digital Object Identifier
    abstract = Column(Text)  # Article abstract
    keywords = Column(String)  # Comma-separated keywords
    publication_date = Column(String)  # Publication date
    url = Column(String)  # URL to the article
    citation = Column(Text)  # Formatted citation string

    projects = relationship(
        "Project",
        secondary=project_reference_link,
        back_populates="references",
    )
    # Many-to-many relationship with users who have access to this reference
    shared_with = relationship(
        "User",
        secondary=reference_owner_link,
        back_populates="shared_references",
    )


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
