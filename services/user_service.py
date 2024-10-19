from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import User, UserSchema
from .utils.database import get_db
from .dependencies import get_current_user

# Import the pydantic models for user data validation
from .schemas import UserCreate, UserUpdate

# Import the passlib library for secure password hashing
from .utils.auth import get_password_hash, verify_password


class UserService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieves a user from the database by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The retrieved User object.
            Raises:
                HTTPException: If no user is found with the given ID.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def create_user(self, user: UserCreate) -> User:
        """
        Creates a new user in the database.

        Args:
            user (UserCreate): The user data to create.

        Returns:
            User: The newly created User object.
            Raises:
                HTTPException: If a user with the same email or username already exists.
        """
        db_user = self.db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        db_user = self.db.query(User).filter(User.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
        hashed_password = get_password_hash(user.password)
        new_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, user_id: int, user: UserUpdate) -> User:
        """
        Updates an existing user in the database.

        Args:
            user_id (int): The ID of the user to update.
            user (UserUpdate): The updated user data.

        Returns:
            User: The updated User object.
            Raises:
                HTTPException: If no user is found with the given ID.
        """
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        """
        Deletes a user from the database.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            None
            Raises:
                HTTPException: If no user is found with the given ID.
        """
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        self.db.delete(db_user)
        self.db.commit()

    def get_user_borrowed_books(self, user_id: int) -> list[BookSchema]:
        """
        Retrieves the borrowing history of a user (list of books they borrowed).

        Args:
            user_id (int): The ID of the user.

        Returns:
            list[BookSchema]: A list of BookSchema objects representing borrowed books.
            Raises:
                HTTPException: If no user is found with the given ID.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        borrowed_books = user.borrowed_books
        return borrowed_books