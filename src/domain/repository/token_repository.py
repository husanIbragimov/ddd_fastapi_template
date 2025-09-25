from abc import ABC, abstractmethod

from domain.entity import UserEntity


class TokenRepository(ABC):
    @abstractmethod
    async def generate_token(self, user: UserEntity) -> str:
        pass
