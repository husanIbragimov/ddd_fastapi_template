from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entity.user_entity import UserEntity
from domain.repository.user_repository import UserRepository
from infrastructure.mappers import user_model_to_entity, user_entity_to_model
from infrastructure.persistence.models import UserModel


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        return await self._get_by_filter(UserModel.email == email)

    async def get_by_uuid(self, uuid: UUID) -> Optional[UserEntity]:
        return await self._get_by_filter(UserModel.uuid == uuid)

    async def _get_by_filter(self, *criteria) -> Optional[UserEntity]:
        result = await self.db.execute(
            select(
                UserModel
            ).where(*criteria))
        user = result.scalar_one_or_none()
        return user_model_to_entity(user) if user else None

    async def save(self, user: UserEntity) -> None:
        model = user_entity_to_model(user)
        self.db.add(model)
        await self.db.commit()
