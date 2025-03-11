from dependency_injector import containers, providers

from src.databases.postgres.client import SQLAlchemyClient
from src.databases.postgres.uow import AsyncDBTransaction
from src.settings import Settings


class Databases(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()  # type: ignore

    postgres = providers.Singleton(
        SQLAlchemyClient,
        settings=config.env.postgres,
    )

    postgres_transaction_uow = providers.ContextLocalSingleton(
        AsyncDBTransaction,
        session=postgres.provided.session,
    )
