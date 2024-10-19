from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Import packages with specific versions as instructed
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

# Define the database engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare base class for models
Base = declarative_base()

# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create database tables (if needed)
def create_tables():
    Base.metadata.create_all(bind=engine)

# Function to query data from database (example)
def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()

# Function to create new data in database (example)
def create_book(db: Session, book: Book):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

# Function to update data in database (example)
def update_book(db: Session, book_id: int, book: Book):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    book_data = book.dict(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

# Function to delete data from database (example)
def delete_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()

# Function to handle database errors
def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Database error")
    return wrapper