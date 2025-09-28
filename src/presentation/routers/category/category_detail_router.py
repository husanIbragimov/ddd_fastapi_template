from fastapi import Depends

from application.usecases import CategoryUseCase
from application.dto import CategoryDTO
from di import container
from presentation.routers.category import category_router
from .schema.category_schema import CategorySchema


@category_router.get("/detail/{category_id}/", status_code=200, response_model=CategoryDTO)
async def get_category(
        category_id: str,
        use_case=Depends(lambda: container.get(CategoryUseCase))
) -> CategorySchema:

    result = await use_case.get_category(category_id)
    return result