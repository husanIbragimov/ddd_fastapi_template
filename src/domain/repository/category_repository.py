from abc import ABC, abstractmethod
from domain.entity.category_entity import CategoryEntity
from domain.entity.paging_entity import PagingEntity


class CategoryRepository(ABC):
    @abstractmethod
    async def create(self, data: CategoryEntity) -> None:
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 10) -> PagingEntity[CategoryEntity]:
        pass

    @abstractmethod
    async def get_by_pk(self, pk: int) -> CategoryEntity | None:
        pass