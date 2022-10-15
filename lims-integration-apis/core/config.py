from typing import Any, Optional
import os
from xmlrpc.client import boolean

from pydantic import BaseSettings, PostgresDsn, validator

from helper.crypto_handler import decrypt


class Settings(BaseSettings):

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALLOWED_APPS = ["LA", "MD"]
    GRANT_TYPE = "client_credentials"
    BACKEND_CORS_ORIGINS: list[Any] = [
        "*",
    ]
    OUTPUT_FOLDER = os.environ.get("OUTPUT_FOLDER", "output_folder")
    LIMS_OUTPUT_BUCKET_NAME = os.environ.get("LIMS_OUTPUT_BUCKET_NAME", "bucket")
    
    LIMS_REGION: str = "us-east-1"
    REPORT_DEBUG: boolean = os.environ.get("REPORT_DEBUG") == "True"
    
    CLIENT_DB_USER: str 
    CLIENT_DB_PASSWORD: str 
    CLIENT_DB_HOST: str 
    CLIENT_DB_NAME: str 
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    class Config:
        env_file = ".env"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        decrypted_password = decrypt(values.get("CLIENT_DB_PASSWORD"), values.get("SECRET_KEY"))
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("CLIENT_DB_USER"),
            password=decrypted_password,
            host=values.get("CLIENT_DB_HOST"),
            path=f"/{values.get('CLIENT_DB_NAME') or ''}",
        )


settings = Settings()
