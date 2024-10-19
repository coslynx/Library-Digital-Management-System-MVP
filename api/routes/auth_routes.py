from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models, schemas
from .utils.auth import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_password_hash,
    verify_password,
)
from .utils.database import get_db
from .dependencies import get_current_user

router = APIRouter(
    tags=["Authentication"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Registers a new user."""
    db_user = models.User(**user.dict())
    db_user.password = get_password_hash(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.Token)
async def login(user: schemas.UserCredentials, db: Session = Depends(get_db)):
    """Logs in an existing user."""
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
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

@router.get("/me", response_model=schemas.User)
async def get_current_user(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Gets the currently authenticated user."""
    return current_user

@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Refreshes the access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        db_user = db.query(models.User).filter(models.User.email == email).first()
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