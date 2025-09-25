from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.entity.category_entity import CategoryEntity
from domain.entity.paging_entity import PagingEntity
from domain.repository.category_repository import CategoryRepository
from infrastructure.persistence.mappers.category_entity_to_model import category_entity_to_model
from infrastructure.persistence.models import CategoryModel


class CategoryRepositoryImpl(CategoryRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: CategoryEntity) -> CategoryModel:
        category_mapper = category_entity_to_model(data)
        self.db.add(category_mapper)
        await self.db.commit()
        await self.db.refresh(category_mapper)
        return category_mapper



    async def list(self, skip: int = 0, limit: int = 10) -> PagingEntity[CategoryEntity]:
        pass

    async def get_by_pk(self, pk: int) -> CategoryEntity | None:
        pass
