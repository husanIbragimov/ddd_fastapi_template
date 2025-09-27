from dataclasses import dataclass
from uuid import UUID


@dataclass
class TagEntity:
    uuid: UUID
    name: dict[str, str]
