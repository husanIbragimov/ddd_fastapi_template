from injector import Module, singleton, Binder, provider
from sqlalchemy.ext.asyncio import AsyncSession
from core.settings import settings
from domain.repository import (
    UserProfileRepository,
    UserRepository,
    CategoryRepository,
)
from domain.services.security import (
    TokenService,
)
from infrastructure.persistence.db_session import DatabaseSession, get_database_session
from infrastructure.persistence.repository import (
    UserRepositoryImpl,
    CategoryRepositoryImpl,
    UserProfileRepositoryImpl,
)
from infrastructure.security import (
    JwtToken
)


class RepositoryModule(Module):
    @provider
    @singleton
    def provide_database(self) -> DatabaseSession:
        return get_database_session(settings.DATABASE_URL)

    @provider
    async def provide_async_session(self, db: DatabaseSession) -> AsyncSession:
        return db.AsyncSessionLocal()

    def configure(self, binder: Binder) -> None:
        binder.bind(TokenService, to=JwtToken, scope=singleton)
        binder.bind(UserProfileRepository, to=UserProfileRepositoryImpl, scope=singleton)
        binder.bind(UserRepository, to=UserRepositoryImpl, scope=singleton)
        binder.bind(CategoryRepository, to=CategoryRepositoryImpl, scope=singleton)
