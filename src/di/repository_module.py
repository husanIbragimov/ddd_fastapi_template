from injector import Module, singleton, Binder, provider
from sqlalchemy.ext.asyncio import AsyncSession

from domain.repository import (
    TagRepository,
    UserRepository,
    CategoryRepository,
    UploadFileRepository,
    UserProfileRepository,
)
from domain.services.security import (
    TokenService,
)
from infrastructure.persistence.db_session import DatabaseSessionManager, get_db_session_manager
from infrastructure.persistence.repository import (
    TagRepositoryImpl,
    UserRepositoryImpl,
    CategoryRepositoryImpl,
    UploadFileRepositoryImpl,
    UserProfileRepositoryImpl,
)
from infrastructure.security import (
    JwtToken
)


class RepositoryModule(Module):
    @provider
    @singleton
    def provide_database_manager(self) -> DatabaseSessionManager:
        """Database session manager - faqat bir marta yaratiladi"""
        return get_db_session_manager()

    @provider
    def provide_async_session(self, db_manager: DatabaseSessionManager) -> AsyncSession:
        """
        Har bir request uchun yangi session yaratadi
        IMPORTANT: Bu singleton emas, har safar yangi session!
        """
        return db_manager.session_factory()

    def configure(self, binder: Binder) -> None:
        binder.bind(TokenService, to=JwtToken, scope=singleton)

        binder.bind(UserProfileRepository, to=UserProfileRepositoryImpl, scope=singleton)
        binder.bind(UserRepository, to=UserRepositoryImpl, scope=singleton)
        binder.bind(CategoryRepository, to=CategoryRepositoryImpl, scope=singleton)
        binder.bind(TagRepository, to=TagRepositoryImpl, scope=singleton)
        binder.bind(UploadFileRepository, to=UploadFileRepositoryImpl, scope=singleton)
