from dishka import FromDishka, provide, Provider, Scope
from faststream.rabbit import RabbitBroker

from src.databases.sqlalchemy.client import SQLAlchemyClient
from src.integrations.faststream.rabbit_mq import rabbit_mq_broker
from src.settings import Settings


class GatewaysProvider(Provider):
    scope = Scope.APP

    @provide()
    def postgres(self, settings: FromDishka[Settings]) -> SQLAlchemyClient:
        return SQLAlchemyClient(settings=settings.env.postgres)

    @provide()
    def rabbitmq(self) -> RabbitBroker:
        return rabbit_mq_broker.broker
