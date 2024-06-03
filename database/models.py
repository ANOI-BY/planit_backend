from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)
    hashed_password = Column(String)

class UsersTables(Base):
    __tablename__ = "users_tables"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    table_id = Column(Integer, ForeignKey("tables.id", ondelete='CASCADE'))

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)

class TableColumn(Base):
    __tablename__ = "columns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    table_id = Column(Integer, ForeignKey("tables.id", ondelete='CASCADE'))


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    column_id = Column(Integer, ForeignKey("columns.id", ondelete='CASCADE'))
    table_id = Column(Integer, ForeignKey("tables.id", ondelete='CASCADE'))
