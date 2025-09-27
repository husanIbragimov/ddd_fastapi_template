from typing import Optional
from uuid import UUID

from injector import inject
from sqlalchemy import select

from domain.entity import UserProfileEntity
from domain.repository import UserProfileRepository
from infrastructure.persistence.db_session import DatabaseSession
from infrastructure.persistence.mappers import user_model_to_entity
from infrastructure.persistence.models import UserModel


class UserRepositoryImpl(UserProfileRepository):
    @inject
    def __init__(self, db: DatabaseSession):
        self.db = db

    async def get_by_uuid(self, uuid: UUID) -> Optional[UserProfileEntity]:
        async with self.db.session_scope() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.uuid == uuid)
            )
            user = result.scalar_one_or_none()
            return user_model_to_entity(user) if user else None
