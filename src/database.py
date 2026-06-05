import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# 1. Читаем URL из переменной окружения Render. 
# Если её нет (например, запускаешь локально), сработает твой старый SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./database.db")

# 2. Корректируем префикс для асинхронной библиотеки asyncpg
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# 3. Создаем движок с динамическим URL
engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_async_session():
    async with async_session_maker() as session:
        yield session