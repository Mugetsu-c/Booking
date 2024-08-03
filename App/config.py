from pydantic_settings import BaseSettings
from pydantic import model_validator

from dotenv import load_dotenv

# Явная загрузка файла .env
load_dotenv()

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: str = None

    @model_validator(mode="before")
    def get_database_url(cls, values):
        # Здесь values должен быть словарем, содержащим все значения полей
        url = f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        values['DATABASE_URL'] = url  # Обновление словаря значений
        return values  # Возвращение обновлённого словаря

    class Config():
        env_file = '.env'

    
settings = Settings()

