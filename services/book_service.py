from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import Book, BookSchema, BookCreateSchema
from .utils.database import get_db
from .dependencies import get_current_user

# Import the pydantic models for book data validation
from .schemas import BookCreate, BookUpdate

# Import the passlib library for secure password hashing
from .utils.auth import get_password_hash, verify_password


class BookService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_book_by_id(self, book_id: int) -> Book:
        """
        Retrieves a book from the database by its ID.

        Args:
            book_id (int): The ID of the book to retrieve.

        Returns:
            Book: The retrieved Book object.
            Raises:
                HTTPException: If no book is found with the given ID.
        """
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return book

    def get_books(self, skip: int = 0, limit: int = 100, title: str = None, author: str = None, isbn: str = None) -> list[Book]:
        """
        Retrieves a list of books based on optional search criteria.

        Args:
            skip (int): The number of books to skip.
            limit (int): The maximum number of books to return.
            title (str): The title of the book to search for.
            author (str): The author of the book to search for.
            isbn (str): The ISBN of the book to search for.

        Returns:
            list[Book]: A list of Book objects matching the search criteria.
        """
        query = self.db.query(Book)
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        if isbn:
            query = query.filter(Book.isbn == isbn)
        books = query.offset(skip).limit(limit).all()
        return books

    def create_book(self, book: BookCreate) -> Book:
        """
        Creates a new book in the database.

        Args:
            book (BookCreate): The book data to create.

        Returns:
            Book: The newly created Book object.
            Raises:
                HTTPException: If a book with the same ISBN already exists.
        """
        db_book = self.db.query(Book).filter(Book.isbn == book.isbn).first()
        if db_book:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book with this ISBN already exists")
        new_book = Book(**book.dict())
        self.db.add(new_book)
        self.db.commit()
        self.db.refresh(new_book)
        return new_book

    def update_book(self, book_id: int, book: BookUpdate) -> Book:
        """
        Updates an existing book in the database.

        Args:
            book_id (int): The ID of the book to update.
            book (BookUpdate): The updated book data.

        Returns:
            Book: The updated Book object.
            Raises:
                HTTPException: If no book is found with the given ID.
        """
        db_book = self.db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        book_data = book.dict(exclude_unset=True)
        for key, value in book_data.items():
            setattr(db_book, key, value)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def delete_book(self, book_id: int):
        """
        Deletes a book from the database.

        Args:
            book_id (int): The ID of the book to delete.

        Returns:
            None
            Raises:
                HTTPException: If no book is found with the given ID.
        """
        db_book = self.db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        self.db.delete(db_book)
        self.db.commit()

    def get_available_books(self, skip: int = 0, limit: int = 100) -> list[Book]:
        """
        Retrieves a list of books that are currently available for borrowing.

        Args:
            skip (int): The number of books to skip.
            limit (int): The maximum number of books to return.

        Returns:
            list[Book]: A list of Book objects that are available.
        """
        books = self.db.query(Book).filter(Book.available == True).offset(skip).limit(limit).all()
        return books

    def borrow_book(self, book_id: int, user_id: int):
        """
        Marks a book as borrowed by a user.

        Args:
            book_id (int): The ID of the book to borrow.
            user_id (int): The ID of the user borrowing the book.

        Returns:
            None
            Raises:
                HTTPException: If the book is not available.
        """
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        if not book.available:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book is not available")
        book.available = False
        book.borrower_id = user_id
        self.db.commit()
        self.db.refresh(book)

    def return_book(self, book_id: int):
        """
        Marks a book as returned.

        Args:
            book_id (int): The ID of the book to return.

        Returns:
            None
            Raises:
                HTTPException: If the book is not borrowed.
        """
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        if book.available:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book is not borrowed")
        book.available = True
        book.borrower_id = None
        self.db.commit()
        self.db.refresh(book)