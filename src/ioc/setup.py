from functools import lru_cache

from dishka import AsyncContainer, make_async_container
from src.ioc.providers import (
    CoreProvider,
    RabbitProvider,
    RepositoriesProvider,
    ServicesProvider,
    SQLAlchemyProvider,
)
from src.settings import Settings


@lru_cache
def setup_ios_container(
    settings: Settings,
    rabbit_provider: RabbitProvider | None = None,
) -> AsyncContainer:
    return make_async_container(
        CoreProvider(settings=settings),
        rabbit_provider or RabbitProvider(),
        SQLAlchemyProvider(),
        RepositoriesProvider(),
        ServicesProvider(),
    )
