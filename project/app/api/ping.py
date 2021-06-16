from fastapi import APIRouter, Depends

from app.config import get_settings, Settings


router = APIRouter()


@router.get("/ping", summary="Check environment settings")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ding": "dong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
