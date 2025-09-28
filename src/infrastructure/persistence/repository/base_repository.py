from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from uuid import UUID

from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from core.exceptions import EntityNotFoundException, InfrastructureException
from core.response import ErrorCode
from domain.entity.paging_entity import PagingEntity

ModelType = TypeVar('ModelType', bound=DeclarativeBase)
EntityType = TypeVar('EntityType')


class BaseRepository(Generic[ModelType, EntityType], ABC):

    def __init__(self, db_session: AsyncSession, model_class: type[ModelType]):
        self.db = db_session
        self.model_class = model_class

    @abstractmethod
    def model_to_entity(self, model: ModelType) -> EntityType:
        """Convert model to entity"""
        pass

    @abstractmethod
    def entity_to_model(self, entity: EntityType) -> ModelType:
        """Convert entity to model"""
        pass

    async def get_by_id(self, entity_id: UUID) -> Optional[EntityType]:
        """Get entity by ID"""
        try:
            result = await self.db.get(self.model_class, entity_id)
            return self.model_to_entity(result) if result else None
        except Exception as e:
            raise InfrastructureException(
                f"Error getting {self.model_class.__name__} by id {entity_id}",
                ErrorCode.DATABASE_ERROR,
                cause=e
            )

    async def list(self, skip: int = 0, limit: int = 100) -> PagingEntity[EntityType]:
        """Get all entities with pagination"""
        try:
            # Get items
            result = await self.db.execute(
                select(self.model_class).offset(skip).limit(limit)
            )
            items = result.scalars().all()

            # Get total count
            total_result = await self.db.execute(
                select(func.count()).select_from(self.model_class)
            )
            total = total_result.scalar_one()

            return PagingEntity[EntityType](
                page=skip // limit + 1,
                size=limit,
                total=total,
                items=[self.model_to_entity(item) for item in items]
            )
        except Exception as e:
            raise InfrastructureException(
                f"Error getting all {self.model_class.__name__}",
                ErrorCode.DATABASE_ERROR,
                cause=e
            )

    async def create(self, entity: EntityType) -> EntityType:
        """Create new entity"""
        try:
            model = self.entity_to_model(entity)
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return self.model_to_entity(model)
        except Exception as e:
            await self.db.rollback()
            raise InfrastructureException(
                f"Error creating {self.model_class.__name__}",
                ErrorCode.DATABASE_ERROR,
                cause=e
            )

    async def update(self, entity_id: UUID, entity: EntityType) -> EntityType:
        """Update existing entity"""
        try:
            existing = await self.db.get(self.model_class, entity_id)
            if not existing:
                raise EntityNotFoundException(self.model_class.__name__, str(entity_id))

            # Update fields from entity
            updated_model = self.entity_to_model(entity)
            for key, value in updated_model.__dict__.items():
                if not key.startswith('_') and hasattr(existing, key):
                    setattr(existing, key, value)

            await self.db.commit()
            await self.db.refresh(existing)
            return self.model_to_entity(existing)
        except Exception as e:
            await self.db.rollback()
            raise InfrastructureException(
                f"Error updating {self.model_class.__name__}",
                ErrorCode.DATABASE_ERROR,
                cause=e
            )

    async def delete(self, entity_id: UUID) -> bool:
        """Delete entity"""
        try:
            result = await self.db.execute(
                delete(self.model_class).where(self.model_class.uuid == entity_id)
            )
            await self.db.commit()
            return result.rowcount > 0
        except Exception as e:
            await self.db.rollback()
            raise InfrastructureException(
                f"Error deleting {self.model_class.__name__}",
                ErrorCode.DATABASE_ERROR,
                cause=e
            )

    async def get_all(self) -> List[EntityType]:
        """Get all entities without pagination"""
        try:
            result = await self.db.execute(
                select(self.model_class)
            )
            items = result.scalars().all()
            return [self.model_to_entity(item) for item in items]
        except Exception as e:
            raise InfrastructureException(
                f"Error getting all {self.model_class.__name__}",
                ErrorCode.DATABASE_ERROR,
                cause=e
            )
