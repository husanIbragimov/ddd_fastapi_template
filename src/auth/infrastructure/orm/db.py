from functools import lru_cache
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base

from core.settings import settings


# === Singleton-like Engine ===
@lru_cache()
def get_engine():
    return create_async_engine(
        settings.DATABASE_URL,
        echo=True,  # Log SQL to stdout
        future=True,
    )


# === Session factory ===
async_session_factory = async_sessionmaker(
    bind=get_engine(),
    expire_on_commit=False,
    class_=AsyncSession
)


# === Dependency for FastAPI routes ===
async def get_db_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with async_session_factory() as session:
        yield session


# === Declarative base for models ===
Base = declarative_base()
