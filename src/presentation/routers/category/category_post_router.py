from fastapi import Depends

from application.dto.category_dto import CategoryDTO
from application.usecases.category_usecase import CategoryUseCase
from di import container
from presentation.routers.category import category_router


@category_router.post("/create", status_code=201, response_model=CategoryDTO)
async def create_category(data: CategoryDTO, use_case=Depends(lambda: container.get(CategoryUseCase))) -> CategoryDTO:
    return await use_case.create_category(data)
