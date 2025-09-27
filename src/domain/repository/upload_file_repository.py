from abc import ABC, abstractmethod

from domain import entity


class UploadFileRepository(ABC):
    @abstractmethod
    async def upload(self, file: bytes, filename: str) -> entity.UploadFileEntity: ...
