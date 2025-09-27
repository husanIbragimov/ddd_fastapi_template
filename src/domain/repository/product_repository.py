from abc import ABC, abstractmethod
from uuid import UUID

from domain import entity


class ProductRepository(ABC):
    @abstractmethod
    async def create(self, product: entity.ProductCreateEntity) -> int: ...

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> entity.ProductDetailEntity: ...

    @abstractmethod
    async def list(self) -> entity.PagingEntity[entity.ProductEntity]: ...

    @abstractmethod
    async def update(self, product_id: UUID, product: entity.ProductCreateEntity) -> int: ...
