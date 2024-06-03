from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

from database import crud, models, schemas
from database.database import SessionLocal, engine

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.post("", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@router.get("", response_model=list[schemas.Task])
def get_tasks(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=offset, limit=limit)
    return tasks

@router.get("/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return crud.get_task(db, task_id=task_id)

@router.get("/column/{column_id}", response_model=list[schemas.Task])
def get_tasks_by_column(column_id: int, db: Session = Depends(get_db)):
    return crud.get_tasks_by_column(db, column_id=column_id)

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return crud.delete_task(db, task_id=task_id)

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    return crud.update_task(db, task_id=task_id, task=task)

@router.put("/{task_id}/move")
def move_task(task_id: int, column_id: int, db: Session = Depends(get_db)):
    return crud.move_task(db, task_id=task_id, column_id=column_id)