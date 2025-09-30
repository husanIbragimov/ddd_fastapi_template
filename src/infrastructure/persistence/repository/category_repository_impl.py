from sqlalchemy.ext.asyncio import AsyncSession

from domain.entity import CategoryEntity
from domain.repository import CategoryRepository
from infrastructure.persistence.mappers import category_entity_to_model, category_model_to_entity
from infrastructure.persistence.models import CategoryModel
from .base_repository import BaseRepository
from injector import inject


class CategoryRepositoryImpl(BaseRepository[CategoryModel, CategoryEntity], CategoryRepository):

    @inject
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model_class=CategoryModel)

    def model_to_entity(self, model: CategoryModel) -> CategoryEntity:
        return category_model_to_entity(model)

    def entity_to_model(self, entity: CategoryEntity) -> CategoryModel:
        return category_entity_to_model(entity)
