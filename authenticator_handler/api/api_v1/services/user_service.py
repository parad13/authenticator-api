from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.user_schema import User, UserCreate

from api import deps
from crud.user_crud import (
    get_current_active_user,
    get_current_user,
    get_user_by_username,
    create_user,
    get_user,
    get_users,
)
from models import user_models
from crud import user_crud, auth_crud

router = APIRouter()


@router.get("/", response_model=list[User])
def read_users(db: Session = Depends(deps.get_db), token=Depends(get_current_user)):
    users = get_users(db)
    return users


@router.post("/", response_model=User)
def create_user(
    user: UserCreate, db: Session = Depends(deps.get_db), token=Depends(get_current_user)
):  # auth_crud.get_auth_token
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already present")
    return user_crud.create_user(db=db, user=user)


@router.get("/{user_id}/", response_model=User)
def read_user(user_id: int, db: Session = Depends(deps.get_db), token=Depends(get_current_user)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user
