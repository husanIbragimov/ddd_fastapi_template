from dataclasses import dataclass
from typing import List
from uuid import UUID

from domain import entity


@dataclass
class ProductDetailEntity:
    uuid: UUID
    name: dict[str, str]
    description: dict[str, str]
    price: float
    stock: int
    category: entity.CategoryEntity
    tags: List[entity.TagEntity]
    images: List[entity.ProjectImageEntity]
