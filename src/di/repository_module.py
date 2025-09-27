from injector import Module, singleton, Binder

from domain.repository import (
    UserProfileRepository,
    UserRepository,
    CategoryRepository,
)
from infrastructure.persistence.repository import (
    UserRepositoryImpl,
    CategoryRepositoryImpl,
    UserProfileRepositoryImpl,
)


class RepositoryModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.bind(UserProfileRepository, to=UserProfileRepositoryImpl, scope=singleton)
        binder.bind(UserRepository, to=UserRepositoryImpl, scope=singleton)
        binder.bind(CategoryRepository, to=CategoryRepositoryImpl, scope=singleton)
