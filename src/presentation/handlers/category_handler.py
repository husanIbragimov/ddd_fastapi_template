from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.dto.category_dto import CategoryDTO
from application.use_case.category_usecase import CategoryUseCase
from core.response.exception_response import ExceptionResponse
from infrastructure.persistence.db import get_db_session
from infrastructure.persistence.repository.category_repository_impl import CategoryRepositoryImpl

category_router = APIRouter(prefix="/category", tags=["category"])


@category_router.post("/create", status_code=201)
async def create_category(req: CategoryDTO, db: AsyncSession = Depends(get_db_session)):
    repo = CategoryRepositoryImpl(db)
    use_case = CategoryUseCase(repo)
    category = await use_case.create_category(req)
    return category
