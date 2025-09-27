from typing import Optional
from uuid import UUID

from sqlalchemy import select

from domain.entity import UserProfileEntity
from domain.repository import UserProfileRepository
from infrastructure.persistence.mappers import profile_model_to_entity
from infrastructure.persistence.models import UserModel
from .base_repository import BaseRepository


class UserProfileRepositoryImpl(UserProfileRepository):
    base_repo: BaseRepository()

    async def get_by_uuid(self, uuid: UUID) -> Optional[UserProfileEntity]:
        async with self.base_repo.db.session_scope() as session:

            result = await session.execute(
                select(UserModel).where(UserModel.uuid == uuid)
            )
            user = result.scalar_one_or_none()
            return profile_model_to_entity(user) if user else None
