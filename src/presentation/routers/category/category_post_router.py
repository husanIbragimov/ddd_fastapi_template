from fastapi import Depends

from application.usecases import CategoryUseCase
from application.dto import CategoryDTO
from core.response import ApiResponse
from di import container
from presentation.routers.category import category_router
from .schema.category_schema import CategorySchema


@category_router.post("/create/", status_code=201)
async def create_category(
        data: CategorySchema,
        use_case=Depends(lambda: container.get(CategoryUseCase))
) -> ApiResponse[CategoryDTO]:

    result = await use_case.create_category(data)
    return result
