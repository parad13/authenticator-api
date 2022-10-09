from fastapi import APIRouter
from ..api_v1.services import login, client_service, user_service

router = APIRouter()
# router.include_router(healthcheck.router, tags=["Health check"])
# router.include_router(report_service.router, tags=["Report APIs"])

router.include_router(login.router, tags=["Access-token"])

router.include_router(client_service.router, prefix="/client", tags=["Client"])

router.include_router(user_service.router, prefix="/users", tags=["User"])
