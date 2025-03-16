from functools import lru_cache

from dishka import AsyncContainer, make_async_container

from src.container.providers import (
    CoreProvider,
    DatabaseProvider,
    GatewaysProvider,
    RepositoriesProvider,
    ServicesProvider,
)
from src.settings import Settings


@lru_cache
def setup_container(
    settings: Settings,
) -> AsyncContainer:
    return make_async_container(
        CoreProvider(settings=settings),
        GatewaysProvider(),
        DatabaseProvider(),
        RepositoriesProvider(),
        ServicesProvider(),
    )
