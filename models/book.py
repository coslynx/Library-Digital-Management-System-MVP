from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, index=True, nullable=False)
    publication_year = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    language = Column(String, nullable=True)
    cover_image_url = Column(String, nullable=True)
    available = Column(Boolean, default=True)
    borrower_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    borrower = relationship("User", backref="borrowed_books")

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"