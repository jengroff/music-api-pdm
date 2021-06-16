import jwt
import os
from typing import List

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, APIRouter, Path
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from app.database.models import User, UserPydantic, UserInPydantic, Status


router = APIRouter()

load_dotenv()

jwt_expire = os.getenv("JWT_EXPIRATION_TIME_MINUTES")
jwt_secret = os.getenv("JWT_SECRET_KEY")
jwt_algo = os.getenv("JWT_ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        user = await User.get(id=payload.get("id"))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return await UserPydantic.from_tortoise_orm(user)


@router.post("/users", response_model=UserPydantic, status_code=201, summary="Create a new user (using email & "
                                                                             "password)")
async def create_user(user: UserInPydantic):
    user_obj = User(
        username=user.username, password_hash=bcrypt.hash(user.password_hash)
    )
    await user_obj.save()
    return await UserPydantic.from_tortoise_orm(user_obj)


@router.post("/token", summary="Login to authenticate and receive JWT")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    user_obj = await UserPydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), jwt_secret)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/users", response_model=List[UserPydantic], summary="Get list of all users in the database")
async def get_users():
    return await UserPydantic.from_queryset(User.all())


@router.delete("/users/{id}", response_model=Status, status_code=200, summary="Delete specific user by User ID")
async def delete_user(
    id: int = Path(..., gt=0),
):
    deleted_count = await User.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User not found")
    return Status(message=f"Deleted user {id}")

