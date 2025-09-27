from dataclasses import dataclass
from uuid import UUID


@dataclass
class ProductEntity:
    uuid: UUID
    name: dict[str, str]
    category_name: str
    price: float
