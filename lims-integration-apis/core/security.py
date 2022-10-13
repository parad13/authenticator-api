from datetime import datetime, timedelta
from typing import Any, Union

from schemas import token

from jose import jwt
import uuid 

from decouple import config
from passlib.context import CryptContext

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = config("ALGORITHM")

def get_jwt_identifier() -> str:
        return str(uuid.uuid4())


def create_access_token(
    role, 
    # jti: str,
    subject: Union[str, Any], 
    expires_time: timedelta = None
) -> str:
    if expires_time:
        expire = datetime.utcnow() + expires_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"jti":get_jwt_identifier(), "exp": expire, "sub": str(subject), "role": role}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

