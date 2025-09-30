from typing import Optional
from uuid import UUID

from injector import inject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import InfrastructureException
from core.response import ErrorCode
from domain.entity import UserEntity
from domain.repository import UserRepository
from infrastructure.persistence.mappers import user_model_to_entity, user_entity_to_model
from infrastructure.persistence.models import UserModel
from .base_repository import BaseRepository


class UserRepositoryImpl(BaseRepository[UserModel, UserEntity], UserRepository):

    @inject
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model_class=UserModel)

    def model_to_entity(self, model: UserModel) -> UserEntity:
        return user_model_to_entity(model)

    def entity_to_model(self, entity: UserEntity) -> UserModel:
        return user_entity_to_model(entity)

    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        return await self._get_by_filter(UserModel.username == username)

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        return await self._get_by_filter(UserModel.email == email)

    async def _get_by_filter(self, *criteria) -> Optional[UserEntity]:
        stmt = select(UserModel).where(*criteria)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        return user_model_to_entity(user) if user else None

    async def save(self, user: UserEntity) -> UUID:
        try:
            stmt = select(UserModel).where(UserModel.email == user.email)
            result = await self.db.execute(stmt)
            if result.scalar_one_or_none():
                raise InfrastructureException(
                    f"User with email {user.email} already exists",
                    ErrorCode.DUPLICATE_ENTITY_ERROR,
                    cause=None
                )

            user_object = user_entity_to_model(user)
            self.db.add(user_object)
            await self.db.commit()
            await self.db.refresh(user_object)
            return user_object.uuid
        except Exception as e:
            await self.db.rollback()
            raise InfrastructureException(
                f"Error saving user with email {user.email}",
                ErrorCode.DATABASE_ERROR,
                cause=e
            )
