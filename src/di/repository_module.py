from injector import Module, singleton, Binder

from domain.repository import (
    UserProfileRepository,
    UserRepository,
    CategoryRepository,
)
from domain.services.security import (
    TokenService,
)
from infrastructure.persistence.repository import (
    UserRepositoryImpl,
    CategoryRepositoryImpl,
    UserProfileRepositoryImpl,
)
from infrastructure.security import (
    JwtToken
)


class RepositoryModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.bind(TokenService, to=JwtToken, scope=singleton)
        binder.bind(UserProfileRepository, to=UserProfileRepositoryImpl, scope=singleton)
        binder.bind(UserRepository, to=UserRepositoryImpl, scope=singleton)
        binder.bind(CategoryRepository, to=CategoryRepositoryImpl, scope=singleton)
