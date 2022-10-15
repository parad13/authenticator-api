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
