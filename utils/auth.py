from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models, schemas
from .utils.config import settings
from .utils.database import get_db

# Define JWT algorithm and secret key
ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.JWT_SECRET

# Create a reusable OAuth2PasswordBearer for JWT authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to generate a JWT token
def create_access_token(data: dict, expires_delta: int = None):
    """
    Generates a JWT token with optional expiration time.

    Args:
        data (dict): The data to encode in the JWT token (e.g., user ID, roles).
        expires_delta (int): The number of seconds the token will be valid for. Defaults to None (no expiration).

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to get the current user from the JWT token
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Retrieves the current user from the JWT token.

    Args:
        db (Session): The SQLAlchemy database session.
        token (str): The JWT token provided in the request header.

    Returns:
        models.User: The user object if the token is valid.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
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
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
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
    return user