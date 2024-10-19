from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import User, UserSchema
from .utils.database import get_db
from .dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)],
)

@router.get("/me", response_model=UserSchema)
async def get_current_user(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == get_current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/me", response_model=UserSchema)
async def update_user(user: UserSchema, db: Session = Depends(get_db)):
    user_data = user.dict(exclude_unset=True)
    db_user = db.query(User).filter(User.id == get_current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user