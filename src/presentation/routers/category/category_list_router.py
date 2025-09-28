from fastapi import Depends

from application.usecases import CategoryUseCase
from application.dto import CategoryDTO, PagingDTO
from di import container
from presentation.routers.category import category_router
from .schema.category_schema import CategorySchema


@category_router.get("/list/", status_code=200, response_model=PagingDTO[CategoryDTO])
async def list_categories(
        skip: int = 1,
        limit: int = 10,
        use_case=Depends(lambda: container.get(CategoryUseCase))
) -> PagingDTO[CategorySchema]:

    result = await use_case.list_categories(skip=skip, limit=limit)
    return result
