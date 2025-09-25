from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from domain.entity import UserEntity
from domain.entity.paging_entity import PagingEntity


class UserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: EmailStr) -> Optional[UserEntity]:
        pass

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID) -> Optional[UserEntity]:
        pass

    @abstractmethod
    async def save(self, user: UserEntity) -> None:
        pass

    @abstractmethod
    async def update(self, user: UserEntity) -> None:
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 10) -> PagingEntity[UserEntity]:
        pass

