from fastapi import APIRouter, Depends, HTTPException
from schemas import report
from api import deps
import crud
from core.config import settings
from schemas.base import TestEcho

router = APIRouter()


@router.get("/health-check", response_model=TestEcho)
async def health_check():
    return TestEcho(message="I am ready!!")
