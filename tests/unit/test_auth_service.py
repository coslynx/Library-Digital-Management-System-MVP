import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api.services.auth_service import AuthService
from api.models.user import User, UserCreate, UserCredentials
from api.utils.database import get_db
from api.utils.auth import get_password_hash, verify_password, create_access_token, ALGORITHM, SECRET_KEY
from api.schemas import Token

# Import necessary packages with specific versions as instructed
import sqlalchemy as sa  # Version 2.0.36
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException, status  # Version 0.115.2
from fastapi.security import OAuth2PasswordBearer  # Version 0.115.2
from jose import JWTError, jwt  # Version 2.7.0
from passlib.context import CryptContext  # Version 1.7.4
from pydantic import BaseModel  # Version 2.9.2
from typing import Optional
from datetime import datetime, timedelta

# Import local modules and functions
from api.utils.config import settings  # Import configuration settings
from api.utils.database import SessionLocal, engine  # Import database functions
from api.utils.auth import (
    ALGORITHM,  # Import JWT algorithm
    SECRET_KEY,  # Import JWT secret key
    create_access_token,  # Import function for JWT token generation
    get_password_hash,  # Import function for password hashing
    verify_password,  # Import function for password verification
)
from api.dependencies import get_current_user  # Import dependency functions


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


@pytest.fixture
def auth_service(db: Session):
    """
    Provides an AuthService instance for testing.

    Args:
        db (Session): A SQLAlchemy database session.

    Returns:
        AuthService: An instance of the AuthService class.
    """
    return AuthService(db=db)


def test_register_user(auth_service: AuthService, db: Session):
    """
    Tests registering a new user.

    Args:
        auth_service (AuthService): An instance of the AuthService class.
        db (Session): A SQLAlchemy database session.
    """
    user_data = UserCreate(username="testuser", email="test@example.com", password="password")

    created_user = auth_service.register_user(user=user_data)

    assert created_user.username == user_data.username
    assert created_user.email == user_data.email
    assert created_user.password == get_password_hash(user_data.password)
    assert db.query(User).filter(User.id == created_user.id).first() is not None


def test_register_user_email_exists(auth_service: AuthService, db: Session):
    """
    Tests registering a new user with an email that already exists.

    Args:
        auth_service (AuthService): An instance of the AuthService class.
        db (Session): A SQLAlchemy database session.
    """
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password=get_password_hash("password"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    user_data = UserCreate(username="newuser", email="test@example.com", password="password")

    with pytest.raises(HTTPException) as exc:
        auth_service.register_user(user=user_data)

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == "Email already registered"


def test_register_user_username_exists(auth_service: AuthService, db: Session):
    """
    Tests registering a new user with a username that already exists.

    Args:
        auth_service (AuthService): An instance of the AuthService class.
        db (Session): A SQLAlchemy database session.
    """
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password=get_password_hash("password"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    user_data = UserCreate(username="testuser", email="newuser@example.com", password="password")

    with pytest.raises(HTTPException) as exc:
        auth_service.register_user(user=user_data)

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == "Username already registered"


def test_login_user(auth_service: AuthService, db: Session):
    """
    Tests logging in an existing user.

    Args:
        auth_service (AuthService): An instance of the AuthService class.
        db (Session): A SQLAlchemy database session.
    """
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password=get_password_hash("password"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    user_data = UserCredentials(email="test@example.com", password="password")

    token = auth_service.login_user(user=user_data)

    assert token["access_token"] is not None
    assert token["token_type"] == "bearer"


def test_login_user_not_found(auth_service: AuthService, db: Session):
    """
    Tests logging in a user that doesn't exist.

    Args:
        auth_service (AuthService): An instance of the AuthService class.
        db (Session): A SQLAlchemy database session.
    """
    user_data = UserCredentials(email="test@example.com", password="password")

    with pytest.raises(HTTPException) as exc:
        auth_service.login_user(user=user_data)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Incorrect username or password"


def test_login_user_incorrect_password(auth_service: AuthService, db: Session):
    """
    Tests logging in with an incorrect password.

    Args:
        auth_service (AuthService): An instance of the AuthService class.
        db (Session): A SQLAlchemy database session.
    """
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password=get_password_hash("password"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    user_data = UserCredentials(email="test@example.com", password="wrongpassword")

    with pytest.raises(HTTPException) as exc:
        auth_service.login_user(user=user_data)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Incorrect username or password"


def test_get_current_user(auth_service: AuthService, db: Session):
    """
    Tests retrieving the currently authenticated user.

    Args:
        auth_service (AuthService): An instance of the AuthService class.
        db (Session): A SQLAlchemy database session.
    """
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password=get_password_hash("password"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Mock the get_current_user dependency to return the user
    with patch("api.services.auth_service.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = user

        retrieved_user = auth_service.get_current_user()

        assert retrieved_user == user


def test_refresh_token(auth_service: AuthService, db: Session):
    """
    Tests refreshing the access token.

    Args:
        auth_service (AuthService): An instance of the AuthService class.
        db (Session): A SQLAlchemy database session.
    """
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password=get_password_hash("password"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate a valid refresh token
    refresh_token = create_access_token(data={"sub": user.email})

    # Mock the oauth2_scheme dependency to return the refresh token
    with patch("api.services.auth_service.oauth2_scheme") as mock_oauth2_scheme:
        mock_oauth2_scheme.return_value = refresh_token

        refreshed_token = auth_service.refresh_token()

        assert refreshed_token["access_token"] is not None
        assert refreshed_token["token_type"] == "bearer"


def test_refresh_token_invalid_token(auth_service: AuthService, db: Session):
    """
    Tests refreshing the access token with an invalid token.

    Args:
        auth_service (AuthService): An instance of the AuthService class.
        db (Session): A SQLAlchemy database session.
    """
    # Mock the oauth2_scheme dependency to return an invalid token
    with patch("api.services.auth_service.oauth2_scheme") as mock_oauth2_scheme:
        mock_oauth2_scheme.return_value = "invalid_token"

        with pytest.raises(HTTPException) as exc:
            auth_service.refresh_token()

        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.value.detail == "Could not validate credentials"


def test_refresh_token_user_not_found(auth_service: AuthService, db: Session):
    """
    Tests refreshing the access token with a token for a user that doesn't exist.

    Args:
        auth_service (AuthService): An instance of the AuthService class.
        db (Session): A SQLAlchemy database session.
    """
    # Generate a refresh token for a non-existent user
    refresh_token = create_access_token(data={"sub": "nonexistent@example.com"})

    # Mock the oauth2_scheme dependency to return the refresh token
    with patch("api.services.auth_service.oauth2_scheme") as mock_oauth2_scheme:
        mock_oauth2_scheme.return_value = refresh_token

        with pytest.raises(HTTPException) as exc:
            auth_service.refresh_token()

        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.value.detail == "Could not validate credentials"