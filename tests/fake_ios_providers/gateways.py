from collections.abc import AsyncGenerator
from typing import Any

from dishka import Scope, provide
from faststream.rabbit import RabbitBroker, TestRabbitBroker
from src.integrations.faststream.rabbit import rabbit_router
from src.ioc.providers import RabbitProvider


class MockRabbitProvider(RabbitProvider):
    @provide(scope=Scope.APP)
    async def rabbit_broker(self) -> AsyncGenerator[RabbitBroker, Any]:
        async with TestRabbitBroker(rabbit_router.broker) as test_broker:
            yield test_broker
