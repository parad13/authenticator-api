from fastapi import APIRouter
from ..api_v1.services import lims_service, login, healthcheck, revoke_service

router = APIRouter()

router.include_router(healthcheck.router, tags=["Health check"])
router.include_router(lims_service.router, tags=["Report APIs"])
router.include_router(login.router, tags=["login"])
router.include_router(revoke_service.router, tags=["Revoke"])
