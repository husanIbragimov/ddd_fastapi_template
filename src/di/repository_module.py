from typing import AsyncGenerator

from injector import Module, singleton, Binder, provider
from sqlalchemy.ext.asyncio import AsyncSession

from domain.repository import (
    UserProfileRepository,
    UserRepository,
    CategoryRepository,
)
from domain.services.security import (
    TokenService,
)
from infrastructure.persistence.db_session import DatabaseSessionManager, get_db_session_manager, get_db
from infrastructure.persistence.repository import (
    UserRepositoryImpl,
    CategoryRepositoryImpl,
    UserProfileRepositoryImpl, BaseRepository
)
from infrastructure.security import (
    JwtToken
)


class RepositoryModule(Module):
    @provider
    @singleton
    def provide_database(self) -> DatabaseSessionManager:
        return get_db_session_manager()

    @provider
    async def provide_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        manager = get_db_session_manager()
        async with manager.session() as session:
            yield session

    def configure(self, binder: Binder) -> None:
        binder.bind(TokenService, to=JwtToken, scope=singleton)

        binder.bind(BaseRepository, to=get_db, scope=singleton)
        binder.bind(UserProfileRepository, to=UserProfileRepositoryImpl, scope=singleton)
        binder.bind(UserRepository, to=UserRepositoryImpl, scope=singleton)
        binder.bind(CategoryRepository, to=CategoryRepositoryImpl, scope=singleton)
