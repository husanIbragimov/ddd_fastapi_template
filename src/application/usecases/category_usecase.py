from typing import Optional

from injector import inject, singleton

from application.dto.category_dto import CategoryDTO
from application.mappers.category_mapper import cat_to_entity
from domain.repository.category_repository import CategoryRepository


@singleton
class CategoryUseCase:

    @inject
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def create_category(self, data: CategoryDTO) -> Optional[CategoryDTO]:
        cat_entity = cat_to_entity(data)
        result =  await self.repository.create(cat_entity)
        return result.to_dto()

    async def get_category(self, category_id) -> Optional[CategoryDTO]:
        result =  await self.repository.get_by_pk(category_id)
        return result.to_dto()
