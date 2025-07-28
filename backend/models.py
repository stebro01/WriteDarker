from sqlalchemy import Column, Integer, String, LargeBinary, Text, ForeignKey
from sqlalchemy.orm import relationship

from .db import Base

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
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    pdf = Column(LargeBinary)
    label = Column(String)
    description = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"))
    notes = Column(String)

    owner = relationship("User", back_populates="documents")
