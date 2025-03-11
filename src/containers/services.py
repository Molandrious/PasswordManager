from dependency_injector import containers, providers

from src import services
from src.containers.repositories import Repositories
from src.settings import Settings


class Services(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()  # type: ignore

    repositories: Repositories = providers.DependenciesContainer()

    password = providers.Factory(
        services.PasswordService,
        password_repository=repositories.password,
        secret_key=config.env.secret_key,
    )
