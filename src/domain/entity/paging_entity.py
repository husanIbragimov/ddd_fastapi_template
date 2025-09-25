from typing import Generic, TypeVar, List

T = TypeVar('T')


class PagingEntity(Generic[T]):
    def __init__(self, page: int, size: int, total: int, items: List[T]):
        self.page = page
        self.size = size
        self.total = total
        self.items = items

    @classmethod
    def new(cls, page: int, size: int, total: int, items: List[T]) -> 'PagingEntity[T]':
        return cls(page, size, total, items)
