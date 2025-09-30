from typing import AsyncGenerator

from injector import Module, singleton, Binder, provider
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from core.settings import settings
from domain.repository import (
    UserProfileRepository,
    UserRepository,
    CategoryRepository,
)
from domain.services.security import (
    TokenService,
)
from infrastructure.persistence.db_session import Database
from infrastructure.persistence.repository import (
    UserRepositoryImpl,
    CategoryRepositoryImpl,
    UserProfileRepositoryImpl
)
from infrastructure.security import (
    JwtToken
)


class RepositoryModule(Module):
    database = Database(settings.DATABASE_URL)
    @provider
    @singleton
    def provide_engine(self) -> create_async_engine:
        return self.database.engine()

    @provider
    async def provide_session(self) -> AsyncSession:
        async with self.database.SessionLocal() as session:
            yield session

    def configure(self, binder: Binder) -> None:
        binder.bind(TokenService, to=JwtToken, scope=singleton)

        binder.bind(UserProfileRepository, to=UserProfileRepositoryImpl, scope=singleton)
        binder.bind(UserRepository, to=UserRepositoryImpl, scope=singleton)
        binder.bind(CategoryRepository, to=CategoryRepositoryImpl, scope=singleton)
