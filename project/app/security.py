from passlib.context import CryptContext
from dotenv import load_dotenv

from fastapi.security import OAuth2PasswordBearer
import jwt

from database.models import JWTUser




load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(e)
        return False


def authenticate_user(user: JWTUser):
