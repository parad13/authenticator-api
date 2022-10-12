from sqlalchemy.orm import Session

from models import client_credentials
from schemas import client_schema

from passlib.context import CryptContext

from core import security

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_client_by_cid(db: Session, client_id: int):
    return (
        db.query(client_credentials.ClientCredentials)
        .filter(client_credentials.ClientCredentials.client_id == client_id)
        .first()
    )


def create_client(db: Session, client: client_schema.Client):
    db_client = client_credentials.ClientCredentials(
        client_id=client.client_id,
        client_secret=security.get_password_hash(client.client_secret),
        role=client.role,
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(client_credentials.ClientCredentials).offset(skip).limit(limit).all()


# async def get_current_client(token: str = Depends(oauth2_scheme)):
#     # get the current user from auth token

#     # define credential exception
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Authentication failed",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         # decode token and extract username and expires data
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#         # username: str = payload.get("sub")
#         # expires = payload.get("exp")
#     except JWTError:
#         raise credentials_exception

#     # validate username
#     # if username is None:
#     #     raise credentials_exception
#     # token_data = token_schema.TokenData(username=username, expires=expires)
#     # users = user_models.User.find(where('name') == token_data.username )
#     # users = get_user_by_username(db, token_data.username)

#     # if user is None:
#     #     raise credentials_exception

#     # check token expiration
#     # if expires is None:
#     #     raise credentials_exception
#     # if datetime.utcnow() > token_data.expires:
#     #     raise credentials_exception
#     # return user
#     return payload
