from uuid import UUID

from injector import inject, singleton

from application.dto import CategoryDTO, PagingDTO
from application.exceptions import errors
from application.mappers import cat_to_entity, cat_to_dto
from core.response import ApiResponse
from domain.repository import CategoryRepository


@singleton
class CategoryUseCase:

    @inject
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def create_category(self, data: CategoryDTO) -> ApiResponse[CategoryDTO | None]:
        try:
            cat_entity = cat_to_entity(data)
            result =  await self.repository.create(cat_entity)
            return ApiResponse.success_response(
                data=result.to_dto(),
                message="Category created successfully"
            )
        except errors.InternalServerError as err:
            return ApiResponse.error_response(
                message=f"Internal Server Error: {err}",
                error_code=500
            )

    async def get_category(self, category_id: UUID) -> ApiResponse[CategoryDTO]:
        result = await self.repository.get_by_uuid(category_id)
        return ApiResponse.success_response(
            data=result.to_dto(),
            message="Category found successfully"
        )

    async def list_categories(self, skip: int = 1, limit: int = 10) -> PagingDTO[CategoryDTO]:
        result = await self.repository.list(skip=skip, limit=limit)

        return PagingDTO.new(
            page=result.page,
            size=result.size,
            total=result.total,
            items=[cat_to_dto(item) for item in result.items]
        )