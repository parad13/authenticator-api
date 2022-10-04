from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from enum import Enum

from api import deps
from schemas import client_credentials
from crud import client_crud
from schemas.client_schema import Client

router = APIRouter()

@router.get("/", response_model=list[Client])
def read_clients(db: Session = Depends(deps.get_db), token = Depends()):
    clients = client_crud.get_clients(db)
    return clients

@router.post("/")
def create_client(client: Client, db: Session = Depends(deps.get_db)):
    db_client = client_crud.get_client_by_cid(db, client.client_id)
    if db_client:
        raise HTTPException(
            status_code=400, 
            detail="Client already present"
        )
    return client_crud.create_client(db, client)


# @router.post("/", response_model = client_credentials.ClientCredentials)
# def create_client(user: client_credentials.ClientCredentials, db: Session = Depends(deps.get_db)): # grant_type:Grant_Type
#     db_client = client_crud.get_client_by_client_id(db, clientid=user.clientid)
#     if db_user:
#         raise HTTPException(
#             status_code=400, 
#             detail="Client already present"
#         )
#     return db_client

# @router.get("/", response_model=list[user_schema.User])
# def read_client(user:UserCreate, db: Session = Depends(get_db)):
#     db_user = get_user_by_username(db, username=user.username)
#     if db_user:
#         return "User already registered"
#     return user_crud.create_user(db, user)

