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

class DatabaseSession(AsyncSession):
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url, echo=True, future=True)
        self.AsyncSessionLocal = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)
        super().__init__(bind=self.engine)

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


# Singleton instance
@lru_cache()
def get_database_session(db_url: str) -> DatabaseSession:
    return DatabaseSession(db_url=db_url)
