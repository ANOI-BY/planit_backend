from pydantic import BaseModel

# User schema

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class UserAuth(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True

# UsersTables schema

class UsersTableBase(BaseModel):
    user_id: int
    table_id: int

class UsersTableCreate(UsersTableBase):
    pass

class UsersTables(BaseModel):
    id: int
    
    class Config:
        orm_mode = True

# Table schema
   
class TableBase(BaseModel):
    title: str

class TableCreate(TableBase):
    pass

class Table(TableBase):
    id: int
    
    class Config:
        orm_mode = True

# Column schema

class ColumnBase(BaseModel):
    title: str
    
    
class ColumnCreate(ColumnBase):
    table_id: int

class ColumnUpdate(ColumnBase):
    pass

class Column(ColumnBase):
    id: int
    table_id: int
    
    class Config:
        orm_mode = True
        

# Task schema
    
class TaskBase(BaseModel):
    pass

class TaskCreate(TaskBase):
    title: str
    description: str
    column_id: int
    table_id: int

class TaskUpdate(TaskBase):
    title: str
    description: str
    column_id: int

class Task(TaskBase):
    id: int
    title: str
    description: str
    column_id: int
    table_id: int
    
    class Config:
        orm_mode = True

class ColumnWithTask(ColumnBase):
    id: int
    table_id: int
    tasks: list[Task]

class TableWithColumns(Table):
    columns: list[ColumnWithTask]

# Auth schema

class AuthEmail(BaseModel):
    email: str
    password: str
    
class AuthUsername(BaseModel):
    username: str
    password: str

class AuthTokenData(BaseModel):
    user_id: int

class AuthSuccessful(BaseModel):
    token: str
    # user: User