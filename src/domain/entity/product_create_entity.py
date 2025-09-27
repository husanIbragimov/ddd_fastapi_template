from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class ProductCreateEntity:
    name: dict[str, str]
    description: dict[str, str]
    price: float
    stock: int
    category_id: UUID
    tags: List[UUID]
    images: List[str]
