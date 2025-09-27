from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class UploadFileEntity:
    uuid: Optional[UUID]
    file_name: str
    url: str
