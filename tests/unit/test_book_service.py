import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.services.book_service import BookService
from api.models.book import Book, BookCreate, BookUpdate
from api.utils.database import get_db
from api.utils.auth import get_password_hash

# Import necessary packages with specific versions as instructed
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

# Import local modules and functions
from api.utils.config import settings
from api.utils.database import SessionLocal, engine
from api.utils.auth import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_password_hash,
    verify_password,
)
from api.dependencies import get_current_user

# Create a fixture for the database session
@pytest.fixture
def db():
    """
    Provides a database session for testing.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = Session()
    yield db
    db.close()

# Create a fixture for the BookService
@pytest.fixture
def book_service(db: Session):
    """
    Provides a BookService instance for testing.

    Args:
        db (Session): A SQLAlchemy database session.

    Returns:
        BookService: An instance of the BookService class.
    """
    return BookService(db=db)

def test_get_book_by_id(book_service: BookService, db: Session):
    """
    Tests retrieving a book by its ID.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book = Book(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1979,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover.jpg",
        available=True,
        borrower_id=None,
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    retrieved_book = book_service.get_book_by_id(book_id=1)

    assert retrieved_book == book

def test_get_book_by_id_not_found(book_service: BookService, db: Session):
    """
    Tests retrieving a book by ID when the book doesn't exist.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    with pytest.raises(HTTPException) as exc:
        book_service.get_book_by_id(book_id=1)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Book not found"

def test_get_books(book_service: BookService, db: Session):
    """
    Tests retrieving a list of books.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book1 = Book(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1979,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover1.jpg",
        available=True,
        borrower_id=None,
    )
    book2 = Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        isbn="0618053262",
        publication_year=1954,
        description="A high fantasy epic",
        genre="Fantasy",
        language="English",
        cover_image_url="https://example.com/cover2.jpg",
        available=True,
        borrower_id=None,
    )
    db.add_all([book1, book2])
    db.commit()
    db.refresh(book1)
    db.refresh(book2)

    books = book_service.get_books()

    assert books == [book1, book2]

def test_get_books_with_title_filter(book_service: BookService, db: Session):
    """
    Tests retrieving a list of books with a title filter.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book1 = Book(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1979,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover1.jpg",
        available=True,
        borrower_id=None,
    )
    book2 = Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        isbn="0618053262",
        publication_year=1954,
        description="A high fantasy epic",
        genre="Fantasy",
        language="English",
        cover_image_url="https://example.com/cover2.jpg",
        available=True,
        borrower_id=None,
    )
    db.add_all([book1, book2])
    db.commit()
    db.refresh(book1)
    db.refresh(book2)

    filtered_books = book_service.get_books(title="Hitchhiker")

    assert filtered_books == [book1]

def test_get_books_with_author_filter(book_service: BookService, db: Session):
    """
    Tests retrieving a list of books with an author filter.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book1 = Book(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1979,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover1.jpg",
        available=True,
        borrower_id=None,
    )
    book2 = Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        isbn="0618053262",
        publication_year=1954,
        description="A high fantasy epic",
        genre="Fantasy",
        language="English",
        cover_image_url="https://example.com/cover2.jpg",
        available=True,
        borrower_id=None,
    )
    db.add_all([book1, book2])
    db.commit()
    db.refresh(book1)
    db.refresh(book2)

    filtered_books = book_service.get_books(author="Adams")

    assert filtered_books == [book1]

def test_get_books_with_isbn_filter(book_service: BookService, db: Session):
    """
    Tests retrieving a list of books with an ISBN filter.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book1 = Book(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1979,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover1.jpg",
        available=True,
        borrower_id=None,
    )
    book2 = Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        isbn="0618053262",
        publication_year=1954,
        description="A high fantasy epic",
        genre="Fantasy",
        language="English",
        cover_image_url="https://example.com/cover2.jpg",
        available=True,
        borrower_id=None,
    )
    db.add_all([book1, book2])
    db.commit()
    db.refresh(book1)
    db.refresh(book2)

    filtered_books = book_service.get_books(isbn="0345391802")

    assert filtered_books == [book1]

def test_create_book(book_service: BookService, db: Session):
    """
    Tests creating a new book.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book_data = BookCreate(
        title="The Restaurant at the End of the Universe",
        author="Douglas Adams",
        isbn="0345391810",
        publication_year=1980,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover3.jpg",
    )

    created_book = book_service.create_book(book=book_data)

    assert created_book.title == book_data.title
    assert created_book.author == book_data.author
    assert created_book.isbn == book_data.isbn
    assert created_book.publication_year == book_data.publication_year
    assert created_book.description == book_data.description
    assert created_book.genre == book_data.genre
    assert created_book.language == book_data.language
    assert created_book.cover_image_url == book_data.cover_image_url
    assert created_book.available is True
    assert created_book.borrower_id is None

def test_create_book_isbn_exists(book_service: BookService, db: Session):
    """
    Tests creating a new book with an ISBN that already exists.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book = Book(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1979,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover1.jpg",
        available=True,
        borrower_id=None,
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    book_data = BookCreate(
        title="The Restaurant at the End of the Universe",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1980,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover3.jpg",
    )

    with pytest.raises(HTTPException) as exc:
        book_service.create_book(book=book_data)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Book with this ISBN already exists"

def test_update_book(book_service: BookService, db: Session):
    """
    Tests updating an existing book.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book = Book(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1979,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover1.jpg",
        available=True,
        borrower_id=None,
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    book_update = BookUpdate(
        title="The Restaurant at the End of the Universe",
        description="A sequel to the Hitchhiker's Guide",
        genre="Fantasy",
        language="Spanish",
        cover_image_url="https://example.com/cover4.jpg",
    )

    updated_book = book_service.update_book(book_id=1, book=book_update)

    assert updated_book.title == book_update.title
    assert updated_book.description == book_update.description
    assert updated_book.genre == book_update.genre
    assert updated_book.language == book_update.language
    assert updated_book.cover_image_url == book_update.cover_image_url

def test_update_book_not_found(book_service: BookService, db: Session):
    """
    Tests updating a book that doesn't exist.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book_update = BookUpdate(
        title="The Restaurant at the End of the Universe",
        description="A sequel to the Hitchhiker's Guide",
        genre="Fantasy",
        language="Spanish",
        cover_image_url="https://example.com/cover4.jpg",
    )

    with pytest.raises(HTTPException) as exc:
        book_service.update_book(book_id=1, book=book_update)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Book not found"

def test_delete_book(book_service: BookService, db: Session):
    """
    Tests deleting a book.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book = Book(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1979,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover1.jpg",
        available=True,
        borrower_id=None,
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    book_service.delete_book(book_id=1)

    retrieved_book = db.query(Book).filter(Book.id == 1).first()

    assert retrieved_book is None

def test_delete_book_not_found(book_service: BookService, db: Session):
    """
    Tests deleting a book that doesn't exist.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    with pytest.raises(HTTPException) as exc:
        book_service.delete_book(book_id=1)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Book not found"

def test_get_available_books(book_service: BookService, db: Session):
    """
    Tests retrieving a list of available books.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book1 = Book(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1979,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover1.jpg",
        available=True,
        borrower_id=None,
    )
    book2 = Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        isbn="0618053262",
        publication_year=1954,
        description="A high fantasy epic",
        genre="Fantasy",
        language="English",
        cover_image_url="https://example.com/cover2.jpg",
        available=False,
        borrower_id=1,
    )
    db.add_all([book1, book2])
    db.commit()
    db.refresh(book1)
    db.refresh(book2)

    available_books = book_service.get_available_books()

    assert available_books == [book1]

def test_borrow_book(book_service: BookService, db: Session):
    """
    Tests borrowing a book.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book = Book(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1979,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover1.jpg",
        available=True,
        borrower_id=None,
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    book_service.borrow_book(book_id=1, user_id=1)

    retrieved_book = db.query(Book).filter(Book.id == 1).first()

    assert retrieved_book.available is False
    assert retrieved_book.borrower_id == 1

def test_borrow_book_not_found(book_service: BookService, db: Session):
    """
    Tests borrowing a book that doesn't exist.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    with pytest.raises(HTTPException) as exc:
        book_service.borrow_book(book_id=1, user_id=1)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Book not found"

def test_borrow_book_not_available(book_service: BookService, db: Session):
    """
    Tests borrowing a book that's already borrowed.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book = Book(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1979,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover1.jpg",
        available=False,
        borrower_id=1,
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    with pytest.raises(HTTPException) as exc:
        book_service.borrow_book(book_id=1, user_id=1)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Book is not available"

def test_return_book(book_service: BookService, db: Session):
    """
    Tests returning a book.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book = Book(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1979,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover1.jpg",
        available=False,
        borrower_id=1,
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    book_service.return_book(book_id=1)

    retrieved_book = db.query(Book).filter(Book.id == 1).first()

    assert retrieved_book.available is True
    assert retrieved_book.borrower_id is None

def test_return_book_not_found(book_service: BookService, db: Session):
    """
    Tests returning a book that doesn't exist.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    with pytest.raises(HTTPException) as exc:
        book_service.return_book(book_id=1)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Book not found"

def test_return_book_already_available(book_service: BookService, db: Session):
    """
    Tests returning a book that's already available.

    Args:
        book_service (BookService): An instance of the BookService class.
        db (Session): A SQLAlchemy database session.
    """
    book = Book(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        publication_year=1979,
        description="A humorous science fiction comedy",
        genre="Science Fiction",
        language="English",
        cover_image_url="https://example.com/cover1.jpg",
        available=True,
        borrower_id=None,
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    with pytest.raises(HTTPException) as exc:
        book_service.return_book(book_id=1)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Book is not borrowed"