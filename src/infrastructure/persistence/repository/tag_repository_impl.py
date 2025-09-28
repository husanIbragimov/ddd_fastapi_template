from domain.entity import TagEntity
from domain.repository import TagRepository
from infrastructure.persistence.db_session import DatabaseSession
from infrastructure.persistence.models import TagModel
from .base_repository import BaseRepository


class TagRepositoryImpl(BaseRepository[TagModel, TagEntity], TagRepository):

    def __init__(self, db_session: DatabaseSession):
        super().__init__(db_session=db_session, model_class=TagModel)

    def model_to_entity(self, model: TagModel) -> TagEntity:
        return TagEntity(uuid=model.uuid, name=model.name)

    def entity_to_model(self, entity: TagEntity) -> TagModel:
        return TagModel(name=entity.name)
