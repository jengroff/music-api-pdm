import jwt
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from app.database.models import User, UserSchema, UserIn_Pydantic


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

    return await UserSchema.from_tortoise_orm(user)


@router.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    user_obj = await UserSchema.from_tortoise_orm(user)

    token = jwt.encode(user_obj.dict(), jwt_secret)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/users", response_model=UserSchema, status_code=201)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(
        username=user.username, password_hash=bcrypt.hash(user.password_hash)
    )
    await user_obj.save()
    return await UserSchema.from_tortoise_orm(user_obj)


@router.get("/users/me", response_model=UserSchema)
async def get_user(user: UserSchema = Depends(get_current_user)):
    return user
