from injector import inject
from sqlalchemy import func, select

from domain.entity.category_entity import CategoryEntity
from domain.entity.paging_entity import PagingEntity
from domain.repository.category_repository import CategoryRepository
from infrastructure.persistence.db_session import DatabaseSession
from infrastructure.persistence.mappers import category_entity_to_model, category_model_to_entity
from infrastructure.persistence.models import CategoryModel


class CategoryRepositoryImpl(CategoryRepository):
    @inject
    def __init__(self, db: DatabaseSession):
        self.db = db

    async def create(self, data: CategoryEntity) -> CategoryModel:
        category_mapper = category_entity_to_model(data)
        async with self.db.session_scope() as session:
            session.add(category_mapper)
            await session.commit()
            return category_mapper

    async def list(self, skip: int = 0, limit: int = 10) -> PagingEntity[CategoryEntity]:
        async with self.db.session_scope() as session:
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
        async with self.db.session_scope() as session:
            result = await session.get(CategoryModel, pk)
            to_entity = category_model_to_entity(result)
            return to_entity
