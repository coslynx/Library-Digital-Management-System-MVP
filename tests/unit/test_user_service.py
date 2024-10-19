import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.services.user_service import UserService
from api.models.user import User, UserCreate, UserUpdate
from api.utils.database import get_db
from api.utils.auth import get_password_hash

@pytest.fixture
def db():
    db = Session()
    yield db
    db.close()

@pytest.fixture
def user_service(db: Session):
    return UserService(db=db)

def test_get_user_by_id(user_service: UserService, db: Session):
    user = User(id=1, username="testuser", email="test@example.com", password=get_password_hash("password"))
    db.add(user)
    db.commit()
    db.refresh(user)

    retrieved_user = user_service.get_user_by_id(user_id=1)

    assert retrieved_user == user

def test_get_user_by_id_not_found(user_service: UserService, db: Session):
    with pytest.raises(HTTPException) as exc:
        user_service.get_user_by_id(user_id=1)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"

def test_create_user(user_service: UserService, db: Session):
    user_data = UserCreate(username="newuser", email="newuser@example.com", password="password")

    created_user = user_service.create_user(user=user_data)

    assert created_user.username == user_data.username
    assert created_user.email == user_data.email
    assert created_user.password == get_password_hash(user_data.password)

def test_create_user_email_exists(user_service: UserService, db: Session):
    user = User(id=1, username="testuser", email="test@example.com", password=get_password_hash("password"))
    db.add(user)
    db.commit()
    db.refresh(user)

    user_data = UserCreate(username="newuser", email="test@example.com", password="password")

    with pytest.raises(HTTPException) as exc:
        user_service.create_user(user=user_data)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Email already registered"

def test_create_user_username_exists(user_service: UserService, db: Session):
    user = User(id=1, username="testuser", email="test@example.com", password=get_password_hash("password"))
    db.add(user)
    db.commit()
    db.refresh(user)

    user_data = UserCreate(username="testuser", email="newuser@example.com", password="password")

    with pytest.raises(HTTPException) as exc:
        user_service.create_user(user=user_data)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Username already registered"

def test_update_user(user_service: UserService, db: Session):
    user = User(id=1, username="testuser", email="test@example.com", password=get_password_hash("password"))
    db.add(user)
    db.commit()
    db.refresh(user)

    user_update = UserUpdate(username="updateduser", email="updated@example.com")

    updated_user = user_service.update_user(user_id=1, user=user_update)

    assert updated_user.username == user_update.username
    assert updated_user.email == user_update.email

def test_update_user_not_found(user_service: UserService, db: Session):
    user_update = UserUpdate(username="updateduser", email="updated@example.com")

    with pytest.raises(HTTPException) as exc:
        user_service.update_user(user_id=1, user=user_update)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"

def test_delete_user(user_service: UserService, db: Session):
    user = User(id=1, username="testuser", email="test@example.com", password=get_password_hash("password"))
    db.add(user)
    db.commit()
    db.refresh(user)

    user_service.delete_user(user_id=1)

    retrieved_user = db.query(User).filter(User.id == 1).first()

    assert retrieved_user is None

def test_delete_user_not_found(user_service: UserService, db: Session):
    with pytest.raises(HTTPException) as exc:
        user_service.delete_user(user_id=1)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"

def test_get_user_borrowed_books(user_service: UserService, db: Session):
    user = User(id=1, username="testuser", email="test@example.com", password=get_password_hash("password"))
    db.add(user)
    db.commit()
    db.refresh(user)

    user.borrowed_books = [MagicMock(id=1), MagicMock(id=2)] 

    borrowed_books = user_service.get_user_borrowed_books(user_id=1)

    assert borrowed_books == [MagicMock(id=1), MagicMock(id=2)]

def test_get_user_borrowed_books_not_found(user_service: UserService, db: Session):
    with pytest.raises(HTTPException) as exc:
        user_service.get_user_borrowed_books(user_id=1)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"