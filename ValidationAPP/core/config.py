from typing import Any, Optional
import os
from xmlrpc.client import boolean

from pydantic import BaseSettings, PostgresDsn, validator

from helper.crypto_handler import decrypt


class Settings(BaseSettings):

    API_V1_STR: str = "/api/v1"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    SECRET_KEY: str
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GRANT_TYPE = "client_credentials"
    REPORT_BUCKET_NAME: str = os.environ.get("REPORT_BUCKET_NAME")
    REPORT_BUCKET_REGION: str = os.environ.get("REPORT_BUCKET_REGION")
    BACKEND_CORS_ORIGINS: list[Any] = [
        "*",
    ]
    REPORT_DEBUG: boolean = os.environ.get("REPORT_DEBUG") == "True"
    # BIOBANK_AUTH_TOKEN: str
    # BIOBANK_AUTH_TOKEN_DECRYPTED: str = decrypt(
    #     os.environ.get("BIOBANK_AUTH_TOKEN"), os.environ.get("SECRET_KEY")
    # )
    # BIOBANK_REQUEST_URL: str

    REPORT_DB_HOST: str
    REPORT_DB_USER: str
    REPORT_DB_PASSWORD: str
    REPORT_DB_NAME: str 
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # mail credentials
    # EMAILS_FROM_EMAIL: str
    EMAIL_TEMPLATES_DIR: str = "email-templates/build"

    class Config:
        env_file = ".env"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        # decrypted_password = decrypt(values.get("REPORT_DB_PASSWORD"), values.get("SECRET_KEY"))
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("REPORT_DB_USER"),
            # password=decrypted_password,
            password=values.get("REPORT_DB_PASSWORD"),
            host=values.get("REPORT_DB_HOST"),
            path=f"/{values.get('REPORT_DB_NAME') or ''}",
        )


settings = Settings()
