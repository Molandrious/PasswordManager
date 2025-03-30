from collections.abc import AsyncIterable

from dishka import FromDishka, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.databases.sqlalchemy.client import SQLAlchemyClient
from src.databases.sqlalchemy.uow import SQLAlchemyUoW
from src.settings import Settings


class SQLAlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def postgres(self, settings: FromDishka[Settings]) -> SQLAlchemyClient:
        return SQLAlchemyClient(settings=settings.env.postgres)

    @provide(scope=Scope.REQUEST)
    async def sqlalchemy_uow(self, postgres: FromDishka[SQLAlchemyClient]) -> SQLAlchemyUoW:
        return postgres.uow

    @provide(scope=Scope.REQUEST)
    async def sqlalchemy_session(self, sqlalchemy_uow: FromDishka[SQLAlchemyUoW]) -> AsyncIterable[AsyncSession]:
        async with sqlalchemy_uow() as session:
            yield session
