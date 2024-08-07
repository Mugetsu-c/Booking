from passlib.context import CryptContext
from pydantic import EmailStr
from datetime import datetime, timedelta

from App.users.DAO import UsersDAO
from App.config import settings

import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str: # Генерация хэша пароля
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
    ) -> bool: # Проверка пароля
    return pwd_context.verify(plain_password, hashed_password)


def create_password_token(data: dict) -> str: # Создание токена авторизации
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_token = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM_KEY
    )
    print(settings.SECRET_KEY, settings.ALGORITHM_KEY, settings.DB_HOST)
    return encoded_token


async def  authenticate_user(
    email: EmailStr, 
    password: str
    ): # Аутентификация пользователя
    user = await UsersDAO.find_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
        return None
    return user