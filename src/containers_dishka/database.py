from collections.abc import AsyncIterable

from dishka import FromDishka, provide, Provider, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.databases.postgres.client import SQLAlchemyClient
from src.settings import Settings


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def postgres(self, settings: FromDishka[Settings]) -> SQLAlchemyClient:
        return SQLAlchemyClient(settings=settings.env.postgres)

    @provide(scope=Scope.REQUEST)
    async def postgres_session(self, postgres: FromDishka[SQLAlchemyClient]) -> AsyncIterable[AsyncSession]:
        async with postgres.uow() as session:
            yield session

