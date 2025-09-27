from uuid import UUID

from sqlalchemy import func, select

from domain import entity
from domain.entity import TagEntity
from domain.repository import TagRepository
from infrastructure.errors import errors
from infrastructure.persistence import models
from .base_repository import BaseRepository


class TagRepositoryImpl(BaseRepository, TagRepository):

    async def create(self, tag: entity.TagEntity) -> UUID:

        async with self.db.session_scope() as session:

            tag_model = models.TagModel(name=tag.name)
            session.add(tag_model)
            await session.commit()
            await session.refresh(tag_model)
            return tag_model.uuid

    async def get_by_id(self, tag_id: UUID) -> errors.RecordNotFoundError | TagEntity:

        async with self.db.session_scope() as session:

            tag_model = await session.get(models.TagModel, tag_id)
            if tag_model is None:
                return errors.RecordNotFoundError("Tag not found")
            return entity.TagEntity(uuid=tag_model.uuid, name=tag_model.name)

    async def list(self, skip: int = 0, limit: int = 10) -> entity.PagingEntity[entity.TagEntity]:

        async with self.db.session_scope() as session:

            result = await session.execute(
                select(models.TagModel).offset(skip).limit(limit)
            )
            items = result.scalars().all()
            total = await session.execute(
                select(func.count()).select_from(models.TagModel)
            )
            total_count = total.scalar_one()
            return entity.PagingEntity[entity.TagEntity](
                page=skip,
                size=limit,
                items=items,
                total=total_count,
            )

    async def update(self, tag_id: UUID, tag: entity.TagEntity) -> UUID:

        async with self.db.session_scope() as session:
            tag_model = await session.get(models.TagModel, tag_id)
            if tag_model is None:
                raise errors.RecordNotFoundError("Tag not found")
            tag_model.name = tag.name
            session.add(tag_model)
            await session.commit()
            await session.refresh(tag_model)
            return tag_model.uuid
