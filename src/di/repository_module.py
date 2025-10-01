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
        """
        Database session manager - faqat bir marta yaratiladi (Singleton)

        IMPORTANT: Bu singleton bo'lishi kerak - connection pool uchun
        """
        return get_db_session_manager()

    @provider
    def provide_async_session(self, db_manager: DatabaseSessionManager) -> AsyncSession:
        """
        Har bir request uchun yangi session yaratadi

        IMPORTANT: Bu singleton EMAS! Har safar yangi session instance qaytaradi.
        Bu session FastAPI dependency injection orqali har bir request uchun
        alohida yaratiladi va avtomatik yopiladi.
        """
        return db_manager.session_factory()

    def configure(self, binder: Binder) -> None:
        # Services - singleton (stateless)
        binder.bind(TokenService, to=JwtToken, scope=singleton)

        # IMPORTANT: Repositories MUST NOT be singleton!
        # Har bir request uchun yangi repository instance yaratiladi
        # Repository ichida session inject qilinadi, va session har request uchun yangi
        # Agar singleton qilsak - bir session barcha request larda ishlatiladi (MEMORY LEAK!)

        binder.bind(UserProfileRepository, to=UserProfileRepositoryImpl)  # NO SINGLETON!
        binder.bind(UserRepository, to=UserRepositoryImpl)  # NO SINGLETON!
        binder.bind(CategoryRepository, to=CategoryRepositoryImpl)  # NO SINGLETON!
        binder.bind(TagRepository, to=TagRepositoryImpl)  # NO SINGLETON!
        binder.bind(UploadFileRepository, to=UploadFileRepositoryImpl)  # NO SINGLETON!
