import os
from pathlib import Path
from typing import ClassVar

from environs import Env
from pydantic_settings import BaseSettings

BASE_DIR: Path = Path(__file__).parent.parent.parent.resolve()

env = Env()
env.read_env(f"{BASE_DIR}/env/.env")


class Settings(BaseSettings):
    SECRET_KEY: str = env.str("SECRET_KEY", "secret")
    TITLE: str = "Auth service"
    DESCRIPTION: str = "Auth service"
    OAUTH_SECRET_KEY: str = "my_dev_secret"
    DB_HOST: str = env.str("POSTGRES_HOST")
    DB_USER: str = env.str("POSTGRES_USER")
    DB_PASSWORD: str = env.str("POSTGRES_PASSWORD")
    DB_NAME: str = env.str("POSTGRES_DB")
    DB_PORT: str = env.str("POSTGRES_PORT")
    DB_SCHEMA: str = env.str("POSTGRES_SCHEMA")

    ALLOWED_ORIGINS: list[str] = ["*"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]
    IS_ALLOWED_CREDENTIALS: bool = bool(env.int("IS_ALLOWED_CREDENTIALS", 0))

    API_PREFIX: str = "/api/v1"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""

    JWT_ALGORITHM: ClassVar[str] = env.str("JWT_ALGORITHM", "Hello")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    VERSION: str = "0.1.0"
    DEBUG: bool = env.bool("DEBUG", False)

    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    @property
    def db_url(self) -> str:
        return (
            f"{self.DB_SCHEMA}+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = f"{BASE_DIR}.env"
        extra = "ignore"

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom values defined in `BackendBaseSettings`.
        """
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }


settings = Settings()
