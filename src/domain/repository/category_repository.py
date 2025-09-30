from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entity.category_entity import CategoryEntity
from domain.entity.paging_entity import PagingEntity


class CategoryRepository(ABC):
    @abstractmethod
    async def create(self, data: CategoryEntity) -> Optional[CategoryEntity]:
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 10) -> PagingEntity[CategoryEntity]:
        pass

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID) -> Optional[CategoryEntity]:
        pass