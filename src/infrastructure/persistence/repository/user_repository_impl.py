from typing import Optional
from uuid import UUID

from sqlalchemy import select

from domain.entity.paging_entity import PagingEntity
from domain.entity.user_entity import UserEntity
from domain.repository.user_repository import UserRepository
from infrastructure.persistence.db_session import DatabaseSession
from infrastructure.persistence.mappers import user_model_to_entity, user_entity_to_model
from infrastructure.persistence.models import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: DatabaseSession):
        self.db = db

    async def update(self, uuid: UUID, user: UserEntity) -> int:
        pass

    async def list(self, skip: int = 0, limit: int = 10) -> PagingEntity[UserEntity]:
        pass

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        return await self._get_by_filter(UserModel.email == email)

    async def get_by_uuid(self, uuid: UUID) -> Optional[UserEntity]:
        return await self._get_by_filter(UserModel.uuid == uuid)

    async def _get_by_filter(self, *criteria) -> Optional[UserEntity]:
        async with self.db.session_scope() as session:
            result = await session.execute(
                select(
                    UserModel
                ).where(*criteria))
            user = result.scalar_one_or_none()
            return user_model_to_entity(user) if user else None

    async def save(self, user: UserEntity) -> None:
        async with self.db.session_scope() as session:
            if await self._get_by_filter(UserModel.email == user.email):
                raise ValueError("Email already exists")
            user_mapper = user_entity_to_model(user)
            session.add(user_mapper)
            await session.commit()
            await session.refresh(user_mapper)
