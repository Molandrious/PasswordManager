from dependency_injector import containers, providers

from src.databases.postgres.client import SQLAlchemyClient
from src.databases.postgres.uow import AsyncDBTransaction


class Databases(containers.DeclarativeContainer):
    config = providers.Configuration()

    postgres = providers.Singleton(
        SQLAlchemyClient,
        settings=config.env.postgres,
    )

    postgres_transaction_uow = providers.ContextLocalSingleton(
        AsyncDBTransaction,
        session=postgres.provided.session,
    )
