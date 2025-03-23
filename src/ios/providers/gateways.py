from dishka import Provider, Scope, provide
from faststream.rabbit import RabbitBroker
from src.integrations.faststream.rabbit import rabbit_router


class RabbitProvider(Provider):
    @provide(scope=Scope.APP)
    def rabbit_broker(self) -> RabbitBroker:
        return rabbit_router.broker
