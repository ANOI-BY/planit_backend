from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status

from sqlalchemy.orm import Session

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Annotated

from database import schemas, crud, database


SECRET_KEY = "3a74866f1a95ed96d66dcb01cccc3373d839ea2b178961c7df939eb921cacf57"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(user_id: int) -> schemas.User:
    db = database.SessionLocal()
    user = crud.get_user(db, user_id=user_id)
    db.close()
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"authorization": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("user_id"))
        if user_id is None:
            raise credentials_exception
        token_data = schemas.AuthTokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = get_user(user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user