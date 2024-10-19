from typing import Union, List, Dict, Any
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import hashlib
import secrets

# Import required libraries for JWT token management.
from jose import jwt
from .config import settings

# Import data models for validation and data representation.
from .models import User, Book

# Import necessary utility functions from other files.
from .exceptions import AuthenticationError, BookNotFoundError

# Import logging module for recording events and errors.
import logging
logger = logging.getLogger(__name__)

# ---  Helper functions for data validation and transformation ---

def validate_email(email: str) -> bool:
    """
    Validates an email address using a regular expression.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    # Implement email validation using a regular expression.
    # Return True if valid, False otherwise.

def validate_isbn(isbn: str) -> bool:
    """
    Validates an ISBN number using a specific algorithm.

    Args:
        isbn (str): The ISBN number to validate.

    Returns:
        bool: True if the ISBN is valid, False otherwise.
    """
    # Implement ISBN validation algorithm.
    # Return True if valid, False otherwise.

def format_date(date_str: str, format: str = "%Y-%m-%d") -> str:
    """
    Formats a date string according to the specified format.

    Args:
        date_str (str): The date string to format.
        format (str): The desired date format. Defaults to "%Y-%m-%d".

    Returns:
        str: The formatted date string.
    """
    try:
        date_obj = datetime.strptime(date_str, format)
        return date_obj.strftime(format)
    except ValueError:
        # Handle invalid date format.
        logger.error(f"Invalid date format: {date_str}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {date_str}",
        )

def generate_unique_id(prefix: str = "LIB") -> str:
    """
    Generates a unique ID with a prefix.

    Args:
        prefix (str): The prefix for the ID. Defaults to "LIB".

    Returns:
        str: The unique ID.
    """
    # Use secrets module to generate random and cryptographically secure IDs.
    random_part = secrets.token_hex(nbytes=8)
    return f"{prefix}-{random_part}"

def hash_password(password: str) -> str:
    """
    Hashes a password using a strong hashing algorithm.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    # Use hashlib module for secure password hashing.
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def get_current_user(token: str = None):
    """
    Retrieves the currently authenticated user from a JWT token.

    Args:
        token (str): The JWT token.

    Returns:
        User: The currently authenticated user.

    Raises:
        AuthenticationError: If the token is invalid or the user is not found.
    """
    if not token:
        raise AuthenticationError(detail="Authentication required")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise AuthenticationError(detail="Invalid token")
        user = User.get_by_email(email)
        if not user:
            raise AuthenticationError(detail="User not found")
        return user
    except JWTError:
        raise AuthenticationError(detail="Invalid token")

def create_access_token(data: Dict[str, Any], expires_delta: timedelta = None):
    """
    Creates a new access token with optional expiration.

    Args:
        data (Dict[str, Any]): The data to be encoded in the token.
        expires_delta (timedelta): The expiration time for the token. Defaults to None (no expiration).

    Returns:
        str: The generated access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_token_data(token: str):
    """
    Retrieves the data encoded in a JWT token.

    Args:
        token (str): The JWT token.

    Returns:
        Dict[str, Any]: The decoded token data.

    Raises:
        AuthenticationError: If the token is invalid.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise AuthenticationError(detail="Invalid token")

def get_book_by_id(book_id: int):
    """
    Retrieves a book from the database by its ID.

    Args:
        book_id (int): The ID of the book.

    Returns:
        Book: The book object.

    Raises:
        BookNotFoundError: If the book is not found.
    """
    book = Book.get_by_id(book_id)
    if not book:
        raise BookNotFoundError(detail="Book not found")
    return book

def check_book_availability(book_id: int):
    """
    Checks the availability status of a book.

    Args:
        book_id (int): The ID of the book.

    Returns:
        bool: True if the book is available, False otherwise.

    Raises:
        BookNotFoundError: If the book is not found.
    """
    book = get_book_by_id(book_id)
    return book.available

def get_borrowed_books(user_id: int):
    """
    Retrieves a list of books borrowed by a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Book]: A list of books borrowed by the user.

    Raises:
        UserNotFoundError: If the user is not found.
    """
    user = User.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user.borrowed_books

# ---  Other helper functions specific to the MVP ---

# Add more helper functions as needed, for example:

# def calculate_overdue_fine(book: Book, days_overdue: int) -> float:
#     """
#     Calculates the overdue fine for a book based on the number of days overdue.
#     """
#     # Implement fine calculation logic.

# def send_overdue_notification(book: Book, user: User):
#     """
#     Sends an overdue notification to the user about a borrowed book.
#     """
#     # Implement notification sending logic.