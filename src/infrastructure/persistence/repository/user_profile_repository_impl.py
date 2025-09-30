from injector import inject
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entity import UserProfileEntity
from domain.repository import UserProfileRepository
from infrastructure.persistence.mappers import profile_model_to_entity
from infrastructure.persistence.models import UserModel
from .base_repository import BaseRepository, EntityType, ModelType


class UserProfileRepositoryImpl(BaseRepository[UserModel, UserProfileEntity], UserProfileRepository):

    @inject
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model_class=UserModel)

    def model_to_entity(self, model: ModelType) -> EntityType:
        return profile_model_to_entity(model)

    def entity_to_model(self, entity: EntityType) -> ModelType:
        pass
