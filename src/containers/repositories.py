from dependency_injector import containers, providers
from dependency_injector.providers import Factory, Resource
from sqlalchemy.ext.asyncio import AsyncSession

from src import repositories
from src.databases.postgres.uow import init_transaction


class Repositories(containers.DeclarativeContainer):
    transaction_uow = providers.Dependency()

    session: Resource[AsyncSession] = providers.Resource(init_transaction, transaction_uow)

    password: Factory[repositories.PasswordRepository] = providers.Factory(
        repositories.PasswordRepository,
        session=session,
    )
