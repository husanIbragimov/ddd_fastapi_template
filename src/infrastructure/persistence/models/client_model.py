from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from domain.entity.enum.client_type import ClientTypeEnum
from .base_model import BaseModel


class ClientModel(BaseModel):
    __tablename__ = "clients"

    client_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    client_secret: Mapped[str] = mapped_column(String, unique=True, index=True)
    redirect_uris: Mapped[str] = mapped_column(String, nullable=True)
    client_type: Mapped[ClientTypeEnum] = mapped_column(String, nullable=False)
    allowed_origins: Mapped[str] = mapped_column(String, nullable=True)
    is_internal: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"<ClientModel client_id={self.client_id} name={self.name} client_type={self.client_type}>"
