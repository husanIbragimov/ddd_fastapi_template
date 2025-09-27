import os
from uuid import UUID

from core.settings import BASE_DIR
from domain.repository import UploadFileRepository
from infrastructure.persistence.models import UploadModel
from .base_repository import BaseRepository


class UploadFileRepositoryImpl(UploadFileRepository):
    base_repo: BaseRepository()

    async def upload(self, file: bytes, filename: str) -> UUID:
        upload_dir = os.path.join(BASE_DIR, "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(file)

        async with self.base_repo.db.session_scope() as session:
            upload_model = UploadModel(url=file_path)
            session.add(upload_model)
            await session.commit()
            await session.refresh(upload_model)
            return upload_model.uuid
