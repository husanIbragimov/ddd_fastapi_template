import os
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import InfrastructureException
from core.response import ErrorCode
from core.settings import BASE_DIR
from domain.repository import UploadFileRepository
from infrastructure.persistence.models import UploadModel
from .base_repository import BaseRepository, EntityType, ModelType


class UploadFileRepositoryImpl(BaseRepository, UploadFileRepository):

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model_class=UploadModel)

    def model_to_entity(self, model: ModelType) -> EntityType:
        ...

    def entity_to_model(self, entity: EntityType) -> ModelType:
        ...

    async def upload(self, file: bytes, filename: str) -> UUID:
        try:
            upload_dir = os.path.join(BASE_DIR, "uploads")
            os.makedirs(upload_dir, exist_ok=True)

            file_path = os.path.join(upload_dir, filename)
            with open(file_path, "wb") as f:
                f.write(file)

            upload_model = UploadModel(url=file_path)
            self.db.add(upload_model)
            await self.db.commit()
            await self.db.refresh(upload_model)
            return upload_model.uuid
        except Exception as e:
            await self.db.rollback()
            raise InfrastructureException(
                f"Error uploading file {filename}",
                ErrorCode.DATABASE_ERROR,
                cause=e
            )
