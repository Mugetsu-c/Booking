from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from App.config import settings


engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True)

async_session_maker = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False)

# Создаем базовый класс для декларативных моделей
Base = declarative_base()