from contextlib import asynccontextmanager
from functools import lru_cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.settings import settings

"""
# Old version - not singleton, creates new engine every time

class DatabaseSession:

    def __init__(self):
        print('DatabaseSession init???????')
        self.engine = AsyncEngine(create_engine(settings.DATABASE_URL, echo=True, future=True))
        self.AsyncSessionLocal = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    @asynccontextmanager
    async def session_scope(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.AsyncSessionLocal()
        try:
            yield session
        finally:
            await session.close()

    @asynccontextmanager
    async def transaction_scope(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.AsyncSessionLocal()
        try:
            async with session.begin():
                yield session
        finally:
            await session.close()
"""

class DatabaseSession:
    _instance = None
    _engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._engine is None:
            self._engine = create_async_engine(
                settings.DATABASE_URL,
                echo=settings.DEBUG,
                pool_size=20,
                max_overflow=30,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            self.AsyncSessionLocal = async_sessionmaker(
                self._engine,
                expire_on_commit=False,
                class_=AsyncSession
            )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.AsyncSessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Singleton instance
@lru_cache()
def get_database_session() -> DatabaseSession:
    return DatabaseSession()
