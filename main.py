from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union, Annotated
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from routes import router as main_router

from routes.auth.methods import auth_user_username

app = FastAPI(
    title='PlanIt API',
    version='0.0.1'
)

origins = [
    "http://192.168.0.194:8000",
    "http://192.168.0.194",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

app.include_router(main_router)

@app.get("/")
def index():
    return {"message": "Hello World"}