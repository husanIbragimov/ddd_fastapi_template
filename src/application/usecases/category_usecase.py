from typing import Optional, Union

from injector import inject, singleton

from application.dto import CategoryDTO, PagingDTO
from application.mappers import cat_to_entity, cat_to_dto
from application.exceptions import errors, ExcResponse
from domain.repository import CategoryRepository


@singleton
class CategoryUseCase:

    @inject
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def create_category(self, data: CategoryDTO) -> Union[CategoryDTO, ExcResponse]:
        try:
            cat_entity = cat_to_entity(data)
            result =  await self.repository.create(cat_entity)
            return result.to_dto()
        except errors.InternalServerError as err:
            return ExcResponse(status_code=500, error=f"Internal Server Error: {err}")

    async def get_category(self, category_id) -> Optional[CategoryDTO]:
        result =  await self.repository.get_by_pk(category_id)
        return result.to_dto()

    async def list_categories(self, skip: int = 0, limit: int = 10) -> PagingDTO[CategoryDTO]:
        result = await self.repository.list(skip=skip, limit=limit)
        print("result", result.items)

        return PagingDTO[CategoryDTO](
            page=skip,
            size=limit,
            total=result.total,
            items=[cat_to_dto(item) for item in result.items]
        )
