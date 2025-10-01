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
        try:

            stmt = select(UserModel).where(*criteria)
            result = await self.db.execute(stmt)
            print("result", result)
            user = result.scalar_one_or_none()
            return user_model_to_entity(user) if user else None
        except Exception as e:
            raise InfrastructureException(
                f"Error getting user by filter {criteria}",
                ErrorCode.DATABASE_ERROR,
                cause=e
            )

    async def save(self, user: UserEntity) -> UUID:
        """
        Save user entity and return the created user

        IMPORTANT: Commit va rollback FastAPI dependency (get_db) tomonidan
        avtomatik bajariladi. Bu yerda faqat flush qilamiz.
        """
        try:
            user_model = user_entity_to_model(user)
            self.db.add(user_model)
            await self.db.commit()
            await self.db.refresh(user_model)
            return user_model.uuid
        except InfrastructureException:
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            raise InfrastructureException(
                f"Error saving user with email {user.email}",
                ErrorCode.DATABASE_ERROR,
                cause=e
            )
