from sqlalchemy.orm import Session
from sqlalchemy import and_
from passlib.context import CryptContext

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# User CRUD

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email, 
        username=user.username, 
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.email = user.email
    db_user.username = user.username
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user


# UsersTables CRUD

def get_users_tables(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UsersTables).offset(skip).limit(limit).all()

def get_users_by_table(db: Session, table_id: int):
    return db.query(models.UsersTables).filter(models.UsersTables.table_id == table_id).all()

def get_tables_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[models.Table]:
    # all_users_tables = db.query(models.UsersTables).filter(models.UsersTables.user_id == user_id).offset(skip).limit(limit).all()
    # tables = db.query(models.Table).join(
    #     models.UsersTables, models.UsersTables.user_id == user_id
    # ).join(
    #     models.Table, models.Table.id == models.UsersTables.table_id
    # ).offset(skip).limit(limit).all()
    tables = db.query(models.Table, models.UsersTables).filter(
        and_(models.UsersTables.user_id == user_id, models.UsersTables.table_id == models.Table.id)
    ).offset(skip).limit(limit).all()
    return list(map(lambda x: x[0], tables))

def create_users_table(db: Session, users_table: schemas.UsersTableCreate):
    db_users_table = models.UsersTables(
        user_id=users_table.user_id,
        table_id=users_table.table_id
    )
    db.add(db_users_table)
    db.commit()
    db.refresh(db_users_table)
    return db_users_table

def delete_users_table(db: Session, user_id: int, table_id: int):
    db_users_table = db.query(models.UsersTables).filter(models.UsersTables.user_id == user_id) \
        .filter(models.UsersTables.table_id == table_id).first()
    db.delete(db_users_table)
    db.commit()
    return db_users_table


# Table CRUD

def get_tables(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Table).offset(skip).limit(limit).all()

def get_table(db: Session, table_id: int):
    table = db.query(models.Table).filter(models.Table.id == table_id).first()
    if not table:
        return table
    else:
        table_with_columns = schemas.TableWithColumns(
            title=table.title,
            id=table.id,
            columns=get_columns_by_table(db, table.id)
        )
        return table_with_columns

def create_table(db: Session, table: schemas.TableCreate):
    db_table = models.Table(
        title=table.title
    )
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def update_table(db: Session, table_id: int, table: schemas.TableCreate):
    db_table = db.query(models.Table).filter(models.Table.id == table_id).first()
    db_table.title = table.title
    db.commit()
    db.refresh(db_table)
    return db_table

def delete_table(db: Session, table_id: int):
    db_table = db.query(models.Table).filter(models.Table.id == table_id).first()
    db.delete(db_table)
    db.commit()
    return db_table


# Column CRUD

def get_columns(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TableColumn, models.Task).offset(skip).limit(limit).all()

def get_column(db: Session, column_id: int):
    column = db.query(models.TableColumn).filter(models.TableColumn.id == column_id).first()
    tasks = get_tasks_by_column(db, column.id)
    column_with_tasks = schemas.ColumnWithTask(
        title=column.title,
        id=column.id,
        table_id=column.table_id,
        tasks=list(
            map(lambda x: schemas.Task(
                id=x.id,
                title=x.title,
                description=x.description,
                column_id=x.column_id,
                table_id=x.table_id
            ), tasks)
        ),
    )
    return column_with_tasks

def get_columns_by_table(db: Session, table_id: int):
    columns = db.query(models.TableColumn).filter(models.TableColumn.table_id == table_id).all()
    columns_with_tasks: list[schemas.ColumnWithTask] = []
    for column in columns:
        tasks = get_tasks_by_column(db, column_id=column.id)
        columns_with_tasks.append(
            schemas.ColumnWithTask(
                id=column.id,
                title=column.title,
                table_id=column.table_id,
                tasks=list(
                    map(lambda x: schemas.Task(
                        id=x.id,
                        title=x.title,
                        description=x.description,
                        column_id=x.column_id,
                        table_id=x.table_id
                    ), tasks)
                ),
            )
        )
    
    return columns_with_tasks
        
def create_column(db: Session, column: schemas.ColumnCreate):
    db_column = models.TableColumn(
        title=column.title,
        table_id=column.table_id
    )
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    return db_column

def update_column(db: Session, column_id: int, column: schemas.ColumnCreate):
    db_column = db.query(models.TableColumn).filter(models.TableColumn.id == column_id).first()
    db_column.title = column.title
    db.commit()
    db.refresh(db_column)
    return db_column

def delete_column(db: Session, column_id: int):
    db_column = db.query(models.TableColumn).filter(models.TableColumn.id == column_id).first()
    db.delete(db_column)
    db.commit()
    return db_column


# Task CRUD

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks_by_column(db: Session, column_id: int):
    return db.query(models.Task).filter(models.Task.column_id == column_id).all()

def get_tasks_by_table(db: Session, table_id: int):
    return db.query(models.Task).filter(models.Task.table_id == table_id).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        column_id=task.column_id,
        table_id=task.table_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db_task.title = task.title
    db_task.description = task.description
    db_task.column_id = task.column_id
    db.commit()
    db.refresh(db_task)
    return db_task

def move_task(db: Session, task_id: int, column_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db_task.column_id = column_id
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db.delete(db_task)
    db.commit()
    return db_task

