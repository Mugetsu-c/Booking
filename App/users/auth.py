from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import EmailStr
import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
    ) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_password_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_token = jwt.encode(
        to_encode, 'asdasdasdasd', 'HS256'
    )
    return encoded_token


async def authenticate_user(
    email: EmailStr, 
    passowrd: str
    ):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
        return None
    return user