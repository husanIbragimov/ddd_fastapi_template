import injector
from .repository_module import RepositoryModule

container = injector.Injector(
    [
        RepositoryModule(),
    ]
)