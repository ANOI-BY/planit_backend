from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import Annotated

from database import crud, models, schemas
from database.database import SessionLocal, engine
from ..dependencies.jwt import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[schemas.User])
def get_users(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=offset, limit=limit)
    return users

@router.get("/get/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/me", response_model=schemas.User)
def get_me_user(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    return current_user