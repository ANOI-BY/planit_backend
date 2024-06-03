from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

from database import crud, models, schemas
from database.database import SessionLocal, engine

from typing import Annotated
from ..dependencies.jwt import get_current_user

router = APIRouter(
    prefix="/tables",
    tags=["tables"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.Table)
def create_table(
    table: schemas.TableCreate, 
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    created_table = crud.create_table(db=db, table=table)
    users_table = crud.create_users_table(
        db=db, 
        users_table=schemas.UsersTableCreate(
            user_id=current_user.id, table_id=created_table.id
        )
    )
    return created_table

@router.get("", response_model=list[schemas.Table])
def get_tables(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    offset: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    tables = crud.get_tables_by_user(db, user_id=current_user.id, skip=offset, limit=limit)
    print(tables)
    return tables

@router.get("/{table_id}", response_model=schemas.TableWithColumns)
def get_table(
    table_id: int, 
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    table = crud.get_table(db, table_id=table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    tables = crud.get_tables_by_user(db, user_id=current_user.id)
    if table_id not in map(lambda x: x.id, tables):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return table

@router.get("/user/{user_id}", response_model=list[schemas.Table])
def get_tables_by_user(
    user_id: int, 
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.get_tables_by_user(db, user_id=user_id)

@router.delete("/{table_id}")
def delete_table(
    table_id: int,
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    table = crud.get_table(db, table_id=table_id)
    users_table = crud.get_users_by_table(db, table_id=table_id)
    if current_user.id not in map(lambda x: x.user_id, users_table):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.delete_table(db, table_id=table_id)

@router.put("/{table_id}", response_model=schemas.Table)
def update_table(
    table_id: int,
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    table: schemas.TableCreate, 
    db: Session = Depends(get_db)
):
    table = crud.get_table(db, table_id=table_id)
    users_table = crud.get_users_by_table(db, table_id=table_id)
    if current_user.id not in map(lambda x: x.user_id, users_table):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.update_table(db, table_id=table_id, table=table)