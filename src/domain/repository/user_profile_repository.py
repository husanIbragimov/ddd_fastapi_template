from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entity import UserProfileEntity


class UserProfileRepository(ABC):

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID) -> Optional[UserProfileEntity]:
        pass
