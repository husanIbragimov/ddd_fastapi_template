from injector import Module, singleton, Binder

from domain.repository import (
    UserRepository,
    CategoryRepository,
)
from infrastructure.persistence.repository import (
    UserRepositoryImpl,
    CategoryRepositoryImpl,
)


class RepositoryModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.bind(type[UserRepository], to=UserRepositoryImpl, scope=singleton)
        binder.bind(type[CategoryRepository], to=CategoryRepositoryImpl, scope=singleton)
