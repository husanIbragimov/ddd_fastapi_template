from uuid import UUID

from fastapi import Depends

from application.usecases import CategoryUseCase
from application.dto import CategoryDTO
from core.response import ApiResponse
from di import container
from presentation.routers.category import category_router
from .schema.category_schema import CategorySchema


@category_router.get("/detail/{category_id}/")
async def get_category(
        category_id: UUID,
        use_case=Depends(lambda: container.get(CategoryUseCase))
) -> ApiResponse[CategoryDTO]:

    result = await use_case.get_category(category_id)
    return result