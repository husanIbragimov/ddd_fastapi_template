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

    IMPORTANT: Bu class Singleton pattern bilan ishlatiladi!
    """

    def __init__(self, db_url: str, echo: bool = False):
        """
        Constructor - Faqat bir marta chaqiriladi

        Args:
            db_url: Database URL (postgresql+asyncpg://...)
            echo: SQL query larni console ga chiqarish
        """
        # Engine yaratish - Connection Pool
        self.engine: AsyncEngine = create_async_engine(
            db_url,
            echo=echo,
            future=True,
            pool_pre_ping=True,  # Connection dead yoki yo'qligini tekshiradi
            pool_size=20,  # Maksimal 20 ta connection
            max_overflow=10,  # Pool to'lganda qo'shimcha 10 ta
            pool_recycle=3600,  # Har 1 soatda connection yangilanadi
            pool_timeout=30,  # Connection kutish vaqti (seconds)
        )

        # Session Factory yaratish
        # Bu factory - har safar yangi AsyncSession instance qaytaradi
        self._session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,  # Commit dan keyin object expire bo'lmasligi
            autoflush=False,  # Manual flush qilish
            autocommit=False,  # Manual commit qilish
        )

    def session_factory(self) -> AsyncSession:
        """
        Session Factory Method

        IMPORTANT: Bu method har safar YANGI AsyncSession qaytaradi!
        Bu DI container tomonidan chaqiriladi.

        Returns:
            AsyncSession: Yangi session instance

        Usage:
            session = db_manager.session_factory()
            # Use session
            await session.commit()
            await session.close()
        """
        return self._session_factory()

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Context Manager - Auto commit/rollback/close

        IMPORTANT: Bu method context manager sifatida ishlatiladi.
        FastAPI Depends() da ishlatish uchun get_db() function mavjud.

        Usage:
            async with db_manager.session() as session:
                # Use session
                # Auto commit if success
                # Auto rollback if error
                # Auto close in finally
        """
        session: AsyncSession = self._session_factory()
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
        Transaction Context Manager - Nested transaction uchun

        Usage:
            async with db_manager.transaction() as session:
                # Multiple operations in single transaction
                await session.execute(...)
                await session.execute(...)
                # Auto commit if all success
        """
        session: AsyncSession = self._session_factory()
        async with session.begin():
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def close(self) -> None:
        """
        Engine ni yopish - Application shutdown da

        Usage:
            @app.on_event("shutdown")
            async def shutdown():
                await db_manager.close()
        """
        if self.engine:
            await self.engine.dispose()

    async def health_check(self) -> bool:
        """
        Database connection health check

        Returns:
            bool: True if connection is healthy

        Usage:
            is_healthy = await db_manager.health_check()
        """
        try:
            async with self.session() as session:
                await session.execute("SELECT 1")
            return True
        except Exception as e:
            print(f"Database health check failed: {e}")
            return False


# Singleton instance - faqat bir marta yaratiladi
_db_session_manager: DatabaseSessionManager | None = None


@lru_cache()
def get_db_session_manager() -> DatabaseSessionManager:
    """
    Singleton pattern - bir marta yaratiladi va qayta ishlatiladi

    IMPORTANT: @lru_cache decorator - faqat bir marta call qiladi

    Returns:
        DatabaseSessionManager: Singleton instance

    Usage:
        db_manager = get_db_session_manager()
        session = db_manager.session_factory()
    """
    global _db_session_manager

    if _db_session_manager is None:
        _db_session_manager = DatabaseSessionManager(
            db_url=settings.DATABASE_URL,
            echo=settings.DEBUG
        )

    return _db_session_manager


# FastAPI dependency uchun
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Depends() uchun dependency

    IMPORTANT: Bu function FastAPI router da ishlatiladi.
    Har bir request uchun yangi session beradi va avtomatik yopadi.

    Usage in FastAPI:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(UserModel))
            return result.scalars().all()

    Yields:
        AsyncSession: Database session for current request
    """
    manager = get_db_session_manager()
    async with manager.session() as session:
        yield session


# Application lifecycle events
async def startup_db() -> None:
    """
    Application startup da chaqiriladi

    Usage:
        @app.on_event("startup")
        async def startup():
            await startup_db()
    """
    db_manager = get_db_session_manager()
    is_healthy = await db_manager.health_check()
    if is_healthy:
        print("✅ Database connection established")
    else:
        print("❌ Database connection failed")
        raise Exception("Database connection failed")


async def shutdown_db() -> None:
    """
    Application shutdown da chaqiriladi

    Usage:
        @app.on_event("shutdown")
        async def shutdown():
            await shutdown_db()
    """
    db_manager = get_db_session_manager()
    await db_manager.close()
    print("✅ Database connection closed")
