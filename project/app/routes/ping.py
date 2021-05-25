from fastapi import APIRouter, Depends
from app.config import get_settings, Settings


router = APIRouter()

@router.get("/")
async def ping(settings: Settings = Depends(get_settings)):
    return {
        "ding": "dong!",
        "environment": settings.environment,
        "testing": settings.testing
    }

