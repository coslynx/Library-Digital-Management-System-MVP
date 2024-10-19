from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import User
from .utils.auth import get_password_hash, verify_password, create_access_token, ALGORITHM, SECRET_KEY
from .utils.database import get_db
from .schemas import UserCreate, UserCredentials, Token
from .dependencies import get_current_user
from typing import Optional

class AuthService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def register_user(self, user: UserCreate) -> User:
        """
        Registers a new user in the database.

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
        new_user = User(username=user.username, email=user.email, password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def login_user(self, user: UserCredentials) -> Token:
        """
        Logs in an existing user.

        Args:
            user (UserCredentials): The user credentials (email, password) for login.

        Returns:
            Token: The access token for the authenticated user.

        Raises:
            HTTPException: If the user is not found or the password does not match.
        """
        db_user = self.db.query(User).filter(User.email == user.email).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": db_user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    def get_current_user(self, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> User:
        """
        Retrieves the currently authenticated user.

        Args:
            db (Session): The database session.
            current_user (User): The currently authenticated user from the JWT token.

        Returns:
            User: The currently authenticated user.
        """
        return current_user

    def refresh_token(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Token:
        """
        Refreshes the access token.

        Args:
            token (str): The refresh token.
            db (Session): The database session.

        Returns:
            Token: The refreshed access token.

        Raises:
            HTTPException: If the refresh token is invalid or the user is not found.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            db_user = self.db.query(User).filter(User.email == email).first()
            if db_user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": db_user.email})
        return {"access_token": access_token, "token_type": "bearer"}