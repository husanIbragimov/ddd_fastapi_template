from asyncpg import InternalServerError
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from domain.entity import CategoryEntity, PagingEntity
from domain.repository import CategoryRepository
from infrastructure.persistence.mappers import category_entity_to_model, category_model_to_entity
from infrastructure.persistence.models import CategoryModel
from .base_repository import BaseRepository


class CategoryRepositoryImpl(CategoryRepository):
    base_repo: BaseRepository()

    async def create(self, data: CategoryEntity) -> CategoryModel:
        try:
            category_mapper = category_entity_to_model(data)

            async with self.base_repo.db.session_scope() as session:
                session.add(category_mapper)
                await session.commit()
                return category_mapper
        except SQLAlchemyError as err:
            raise InternalServerError from err

    async def list(self, skip: int = 0, limit: int = 10) -> PagingEntity[CategoryEntity]:

        async with self.base_repo.db.session_scope() as session:
            result = await session.execute(
                CategoryModel.__table__.select().offset(skip).limit(limit)
            )
            items = result.scalars().all()
            total = await session.execute(
                select(func.count()).select_from(CategoryModel)
            )
            total_count = total.scalar_one()
            return PagingEntity[CategoryEntity](page=skip, size=limit, total=total_count, items=items)

    async def get_by_pk(self, pk: int) -> CategoryEntity | None:

        async with self.base_repo.db.session_scope() as session:
            result = await session.get(CategoryModel, pk)
            to_entity = category_model_to_entity(result)
            return to_entity
