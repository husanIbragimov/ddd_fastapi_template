from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain import entity


class TagRepository(ABC):
    @abstractmethod
    async def create(self, tag: entity.TagEntity) -> UUID: ...

    @abstractmethod
    async def get_by_id(self, tag_id: UUID) -> Optional[entity.TagEntity]: ...

    @abstractmethod
    async def list(self, skip: int = 1, limit: int = 10) -> entity.PagingEntity[entity.TagEntity]: ...

    @abstractmethod
    async def update(self, tag_id: UUID, tag: entity.TagEntity) -> UUID: ...
