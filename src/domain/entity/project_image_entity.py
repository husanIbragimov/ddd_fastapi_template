from dataclasses import dataclass
from uuid import UUID


@dataclass
class ProjectImageEntity:
    uuid: UUID
    image_url: str