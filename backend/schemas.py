from typing import Optional
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
        orm_mode = True

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

class DocumentCreate(DocumentBase):
    pass

class DocumentRead(DocumentBase):
    id: int

    class Config:
        orm_mode = True
