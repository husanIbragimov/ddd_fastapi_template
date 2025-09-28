from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class PagingDTO(BaseModel, Generic[T]):
    page: int
    size: int
    total: int
    items: List[T]

    @classmethod
    def new(cls, page: int, size: int, total: int, items: List[T]) -> 'PagingDTO[T]':
        return cls(page=page, size=size, total=total, items=items)
