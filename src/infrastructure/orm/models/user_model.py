from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    _hashed_password: Mapped[str] = mapped_column("hashed_password", String)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    passport_series: Mapped[str] = mapped_column(String)
    passport_number: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    phone_number: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    date_joined: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    def set_hashed_password(self, password: str):
        self._hashed_password = password
