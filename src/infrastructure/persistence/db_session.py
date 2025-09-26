from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from core.settings import settings


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
