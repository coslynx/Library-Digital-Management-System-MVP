from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    borrowed_books = relationship("BorrowingRecord", backref="borrower")

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True