from datetime import timedelta
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.param_functions import Form
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
import crud
from core.logger_config import ErrorType, log_handler
from helper.crypto_handler import decrypt
from schemas import Token
from api import deps
from jose import jwt
from fastapi_jwt_auth import AuthJWT
from core.config import settings
from pydantic import BaseModel


router = APIRouter()

INVALID_CREDENTIALS = "Invalid credentials"

class OAuth2ClientCredentialsRequestForm:
    """
    Expect OAuth2 client credentials as form request parameters
    """

    def __init__(
        self,
        grant_type: str = Form(None, regex="^(client_credentials|refresh_token|password)$"),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


@router.post(
    "/oauth/access-token",
    response_model=Token,
    include_in_schema=False,
)
def login_access_token(
    *,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(deps.get_db),
    form_data: OAuth2ClientCredentialsRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    payload: dict = jsonable_encoder(form_data)
    app_client = crud.client_credentials.get_client_credentials(db=db, client_credentials=form_data)
    if not app_client:
        log_handler(INVALID_CREDENTIALS, ErrorType.ERROR, request_payload=str(payload))
        raise HTTPException(status_code=400, detail=INVALID_CREDENTIALS)
    try:
        decrypted_secret = decrypt(app_client.client_secret, settings.SECRET_KEY)
    except HTTPException as e:
        log_handler(e.detail, ErrorType.ERROR, request_payload=payload)
        db.rollback()
        raise

    if form_data.client_secret != decrypted_secret:
        log_handler(INVALID_CREDENTIALS, ErrorType.ERROR, request_payload=str(payload))
        raise HTTPException(status_code=400, detail=INVALID_CREDENTIALS)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    role = app_client.role
    access_token = Authorize.create_access_token(
        "subject", 
        expires_time=access_token_expires, 
        user_claims={"role": role}
    )
    return {
        "access_token": access_token, 
        "token_type": "Bearer"
    }
