from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()

@router.post("/token")
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):