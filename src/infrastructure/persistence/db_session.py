from contextlib import asynccontextmanager
from functools import lru_cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine
)

from core.settings import settings


class DatabaseSessionManager:
    """
    Singleton Database Session Manager
    - Connection pooling bilan optimal ishlaydi
    - Memory leak oldini oladi
    - Har bir request uchun yangi session beradi
    """

    def __init__(self, db_url: str, echo: bool = False):
        # Engine yaratish - faqat bir marta
        self.engine: AsyncEngine = create_async_engine(
            db_url,
            echo=echo,
            future=True,
            pool_pre_ping=True,  # Connection dead yoki yo'qligini tekshiradi
            pool_size=20,  # Maksimal 20 ta connection
            max_overflow=10,  # Pool to'lganda qo'shimcha 10 ta
            pool_recycle=3600,  # Har 1 soatda connection yangilanadi
            pool_timeout=30,  # Connection kutish vaqti
            connect_args={
                "server_settings": {"application_name": "auth_service"},
                "timeout": 30,
            }
        )

        # Session factory - har bir request uchun yangi session yaratadi
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,  # Commit dan keyin object expire bo'lmasligi
            autoflush=False,  # Manual flush qilish
            autocommit=False,  # Manual commit qilish
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Context manager - har bir request uchun yangi session
        Avtomatik commit/rollback bilan
        """
        session: AsyncSession = self.session_factory()
        try:
            yield session
            await session.commit()  # Muvaffaqiyatli bo'lsa commit
        except Exception:
            await session.rollback()  # Xato bo'lsa rollback
            raise
        finally:
            await session.close()  # Har doim session yopiladi

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Transaction context manager - nested transaction uchun
        """
        session: AsyncSession = self.session_factory()
        async with session.begin():
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def close(self) -> None:
        """Engine ni yopish - application shutdown da"""
        if self.engine:
            await self.engine.dispose()


# Singleton instance - faqat bir marta yaratiladi
@lru_cache()
def get_db_session_manager() -> DatabaseSessionManager:
    """
    Singleton pattern - bir marta yaratiladi va qayta ishlatiladi
    """
    return DatabaseSessionManager(
        db_url=settings.DATABASE_URL,
        echo=settings.DEBUG
    )


# FastAPI dependency uchun
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Depends() uchun dependency
    Har bir request uchun yangi session beradi va avtomatik yopadi
    """
    manager = get_db_session_manager()
    async with manager.session() as session:
        yield session
