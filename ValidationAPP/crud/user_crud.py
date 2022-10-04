from sqlalchemy.orm import Session

from typing import Union
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.context import CryptContext

from jose import JWTError, jwt

from decouple import config

from models import user_models
from schemas import token, user_schema
from core import security


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ALGORITHM = config('ALGORITHM')
SECRET_KEY = config('SECRET_KEY')

def get_user(db: Session, user_id: int):
    return db.query(user_models.User).filter(user_models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(user_models.User).filter(user_models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schema.UserCreate):
    db_user = user_models.User(username=user.username, password=security.get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # get the current user from auth token

    # define credential exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication failed",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # decode token and extract username and expires data
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    #Role checking
    if "MD" not in payload.get("role"):
        raise HTTPException(
            status_code=404,
            detail="Method Not allowed for UserAPI",
            headers={"X-Error": "There goes my error"},
        )
    return payload

async def get_current_active_user(current_user: user_schema.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

