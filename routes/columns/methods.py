from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

from database import crud, models, schemas
from database.database import SessionLocal, engine

from typing import Annotated
from ..dependencies.jwt import get_current_user

router = APIRouter(
    prefix="/columns",
    tags=["columns"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.Column)
def create_column(column: schemas.ColumnCreate, db: Session = Depends(get_db)):
    return crud.create_column(db=db, column=column)

@router.get("", response_model=list[schemas.Column])
def get_columns(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    columns = crud.get_columns(db, skip=offset, limit=limit)
    return columns

@router.get("/{column_id}", response_model=schemas.ColumnWithTask)
def get_column(column_id: int, db: Session = Depends(get_db)):
    return crud.get_column(db, column_id=column_id)

@router.get("/table/{table_id}", response_model=list[schemas.ColumnWithTask])
def get_columns_by_table(
    table_id: int, 
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    return crud.get_columns_by_table(db, table_id=table_id)

@router.delete("/{column_id}")
def delete_column(column_id: int, db: Session = Depends(get_db)):
    return crud.delete_column(db, column_id=column_id)

@router.put("/{column_id}", response_model=schemas.Column)
def update_column(column_id: int, column: schemas.ColumnUpdate, db: Session = Depends(get_db)):
    return crud.update_column(db, column_id=column_id, column=column)