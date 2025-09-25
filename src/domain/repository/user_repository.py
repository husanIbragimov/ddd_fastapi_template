from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from domain.entity import UserEntity


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

class TokenRepository(ABC):
    @abstractmethod
    async def generate_token(self, user: UserEntity) -> str:
        pass
