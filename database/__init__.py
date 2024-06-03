from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

from . import models
from .database import engine
from dependencies import get_token_header

models.Base.metadata.create_all(bind=engine)