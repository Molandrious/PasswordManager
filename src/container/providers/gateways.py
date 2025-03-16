from dishka import FromDishka, provide, Provider, Scope

from src.databases.sqlalchemy.client import SQLAlchemyClient
from src.settings import Settings


class GatewaysProvider(Provider):
    scope = Scope.APP

    @provide()
    def postgres(self, settings: FromDishka[Settings]) -> SQLAlchemyClient:
        return SQLAlchemyClient(settings=settings.env.postgres)
