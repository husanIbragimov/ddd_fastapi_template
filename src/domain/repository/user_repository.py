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
    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    async def save(self,  user: UserEntity) -> UUID:
        pass

    @abstractmethod
    async def update(self, uuid: UUID, user: UserEntity) -> int:
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 10) -> PagingEntity[UserEntity]:
        pass

