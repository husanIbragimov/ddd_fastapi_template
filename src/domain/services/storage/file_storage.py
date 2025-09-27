from abc import ABC, abstractmethod


class FileStorage(ABC):
    @abstractmethod
    async def upload(self, folder: str, local_file_path: str) -> str:
        pass

    @abstractmethod
    async def save_temp_file(self, file_data: bytes, file_extension: str) -> str:
        pass

    @abstractmethod
    async def get_presigned_url(self, file_path: str, expires_in: int = 3600) -> str:
        pass
