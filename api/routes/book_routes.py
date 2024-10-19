from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import Book, BookSchema, BookCreateSchema
from .utils.database import get_db
from .dependencies import get_current_user

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    dependencies=[Depends(get_current_user)],
)

@router.get("/", response_model=list[BookSchema])
async def get_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    title: str = None,
    author: str = None,
    isbn: str = None,
):
    """Retrieves a list of books based on optional search criteria."""
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if isbn:
        query = query.filter(Book.isbn == isbn)
    books = query.offset(skip).limit(limit).all()
    return books

@router.get("/{book_id}", response_model=BookSchema)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """Retrieves details for a specific book by its ID."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router.post("/", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreateSchema, db: Session = Depends(get_db)):
    """Creates a new book record in the database."""
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.put("/{book_id}", response_model=BookSchema)
async def update_book(book_id: int, book: BookSchema, db: Session = Depends(get_db)):
    """Updates an existing book record."""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    book_data = book.dict(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Deletes a book record from the database."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(book)
    db.commit()