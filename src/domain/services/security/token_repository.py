from abc import ABC, abstractmethod
from typing import Optional

from datetime import timedelta


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, payload: dict, expires_delta: Optional[timedelta] = None) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass
