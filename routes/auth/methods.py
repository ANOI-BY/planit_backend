from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

from database import crud, models, schemas, translator
from database.database import SessionLocal, engine

from ..dependencies.jwt import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/email", response_model=schemas.AuthSuccessful)
def auth_user_email(user: schemas.AuthEmail, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    token_data = schemas.AuthSuccessful(
        token=create_access_token({"user_id": db_user.id}),
        # user=translator.from_model_user_to_schema_user(db_user)
    )
    
    return token_data

@router.post("/username", response_model=schemas.AuthSuccessful)
def auth_user_username(user: schemas.AuthUsername, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    token_data = schemas.AuthSuccessful(
        token=create_access_token({"user_id": db_user.id}),
        # user=translator.from_model_user_to_schema_user(db_user)
    )
    
    return token_data

@router.post('/register', response_model=schemas.AuthSuccessful)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = crud.create_user(db=db, user=user)
    
    token_data = schemas.AuthSuccessful(
        token=create_access_token({"user_id": db_user.id}),
        # user=translator.from_model_user_to_schema_user(db_user)
    )
    
    return token_data