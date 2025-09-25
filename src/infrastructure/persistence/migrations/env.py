from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from infrastructure.persistence.models import BaseModel
from core.settings import settings

# Alembic Config object
config = context.config

# Log konfiguratsiya
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# metadata (migration uchun)
target_metadata = BaseModel.metadata

# URL ni async emas, balki sync qilamiz
def get_sync_url():
    return settings.DATABASE_URL.replace("+asyncpg", "+psycopg2")

def run_migrations_offline():
    """Offline rejim (sql fayl yozish)."""
    url = get_sync_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Online rejim (real migration)."""
    connectable = engine_from_config(
        {"sqlalchemy.url": get_sync_url()},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
