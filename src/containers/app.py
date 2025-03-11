from dependency_injector import containers, providers

from src.containers.database import Databases
from src.containers.repositories import Repositories
from src.containers.services import Services
from src.settings import get_settings


class App(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[get_settings()])

    databases: Databases = providers.Container(
        Databases,
        config=config,
    )

    repositories: Repositories = providers.Container(
        Repositories,
        transaction_uow=databases.postgres.provided.get_transaction_uow,
    )

    services: Services = providers.Container(
        Services,
        repositories=repositories,
        config=config,
    )
