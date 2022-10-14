from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import settings
from api.api_v1.router import router as api_router
from models import Base
from db_pg.session import engine
from mangum import Mangum

from starlette.middleware import Middleware
from starlette_context import context, plugins
from starlette_context.middleware import RawContextMiddleware
from fastapi_jwt_auth import AuthJWT
from core.logger_config import logger
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

middleware = [
    Middleware(
        RawContextMiddleware, plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin())
    )
]

app = FastAPI(middleware=middleware)

# set denylist enabled to True
# you can set to check access or refresh token or even both of them
class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access","refresh"}

@AuthJWT.load_config
def get_config():
    return Settings()

# app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
# jwt = JWTManager(app)

app.include_router(api_router, prefix=settings.API_V1_STR)
handler = Mangum(app)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Phenomix",
        version="1.0.0",
        description="OpenAPI schema",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Centralised authentication api
# Logging and monitarisation 
