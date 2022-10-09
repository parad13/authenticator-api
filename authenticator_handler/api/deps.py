from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2, OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from jose import jwt
from starlette_context import context

from core import security
from core.config import settings
from db_pg.session import SessionLocal
from core.logger_config import ErrorType, log_handler

TOKEN_EXPIRED = "Token has expired"
INVALID_SIGNATURE = "Invalid signature"


class OAuth2ClientCredentials(OAuth2):
    """
    Implement OAuth2 client_credentials workflow.

    This is modeled after the OAuth2PasswordBearer and OAuth2AuthorizationCodeBearer
    classes from FastAPI, but sets auto_error to True to avoid uncovered branches.
    See https://github.com/tiangolo/fastapi/issues/774 for original implementation,
    and to check if FastAPI added a similar class.

    See RFC 6749 for details of the client credentials authorization grant.
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict[str, str]] = None,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=True)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")

        scheme_param = get_authorization_scheme_param(authorization)
        scheme: str = scheme_param[0]
        param: str = scheme_param[1]

        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return param


reusable_oauth2 = OAuth2ClientCredentials(f"{settings.API_V1_STR}/oauth/access-token")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def token_filter(token: str = Depends(reusable_oauth2)) -> bool:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
    except jwt.ExpiredSignatureError:
        log_handler(TOKEN_EXPIRED, ErrorType.ERROR, context.data["X-Request-ID"])
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has expired",
        )
    except jwt.JWTError:
        log_handler(INVALID_SIGNATURE, ErrorType.ERROR, context.data["X-Request-ID"])
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=INVALID_SIGNATURE,
        )
    return payload
