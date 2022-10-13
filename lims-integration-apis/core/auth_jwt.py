from datetime import datetime, timedelta
from typing import Any, Union, Optional, Sequence, Dict

from schemas import token

from jose import jwt
from fastapi_jwt_auth.auth_config import AuthConfig

from decouple import config
from passlib.context import CryptContext
import uuid

from fastapi_jwt_auth.exceptions import (
    InvalidHeaderError,
    CSRFError,
    JWTDecodeError,
    RevokedTokenError,
    MissingTokenError,
    AccessTokenRequired,
    RefreshTokenRequired,
    FreshTokenRequired
)

from core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = config("ALGORITHM")

class AuthJWT(AuthConfig):

    # def _verify_jwt_in_request(
    #     self,
    #     token: str,
    #     type_token: str,
    #     token_from: str,
    #     fresh: Optional[bool] = False
    # ) -> None:
    #     if type_token not in ['access','refresh']:
    #         raise ValueError("type_token must be between 'access' or 'refresh'")
    #     if token_from not in ['headers','cookies','websocket']:
    #         raise ValueError("token_from must be between 'headers', 'cookies', 'websocket'")

        # if not token:
        #     if token_from == 'headers':
        #         raise MissingTokenError(status_code=401,message="Missing {} Header".format(self._header_name))
        #     if token_from == 'websocket':
        #         raise MissingTokenError(status_code=1008,message="Missing {} token from Query or Path".format(type_token))

        # if self.get_raw_jwt(token)['type'] != type_token:
        #     msg = "Only {} tokens are allowed".format(type_token)
        #     if type_token == 'access':
        #         raise AccessTokenRequired(status_code=422,message=msg)
        #     if type_token == 'refresh':
        #         raise RefreshTokenRequired(status_code=422,message=msg)

        # if fresh and not self.get_raw_jwt(token)['fresh']:
        #     raise FreshTokenRequired(status_code=401,message="Fresh token required")

    # def _get_jwt_identifier(self) -> str:
    # return str(uuid.uuid4())

    def create_access_token(
        self,
        role, 
        subject: Union[str, Any], 
        expires_delta: timedelta = None
    ) -> str:
    
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        # Data section
        reserved_claims = {
            "jti": self._get_jwt_identifier(),
            "exp": expire, 
            "sub": str(subject), 
            "role": role
        }

        return jwt.encode(
            {**reserved_claims},
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
            # headers=headers
        )

    
    # def _get_jwt_identifier(self) -> list:
    #     return str(uuid.uuid4())
    
 
    




