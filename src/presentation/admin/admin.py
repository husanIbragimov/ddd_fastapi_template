from sqladmin import Admin
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine

from core.settings import settings
from presentation.app import app

engine = AsyncEngine(create_engine(settings.DATABASE_URL, echo=True, future=True))
admin = Admin(app, engine)
