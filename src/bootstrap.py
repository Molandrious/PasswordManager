from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import cast

from dishka import AsyncContainer, make_async_container
from dishka.integrations import fastapi
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.containers_dishka.core import CoreProvider
from src.containers_dishka.database import DatabaseProvider
from src.containers_dishka.repositories import RepositoriesProvider
from src.containers_dishka.services import ServicesProvider
from src.settings import Settings
from src.transport.rest import FastAPIContainerized
from src.transport.rest.setup import setup_error_handlers, setup_middlewares, setup_routers


@asynccontextmanager
async def _lifespan(
    app: FastAPIContainerized,
) -> AsyncGenerator[None]:
    yield
    await app.state.dishka_container.close()


def setup_app() -> FastAPI:
    app = FastAPI(
        lifespan=_lifespan,
        default_response_class=ORJSONResponse,
    )

    setup_routers(app)
    setup_middlewares(app)
    setup_error_handlers(app)

    return app


def setup_container(
    settings: Settings | None = None,
) -> AsyncContainer:
    return make_async_container(
        CoreProvider(settings=settings or Settings()),
        DatabaseProvider(),
        RepositoriesProvider(),
        ServicesProvider(),
    )


def make_app(
    container: AsyncContainer | None = None,
) -> FastAPIContainerized:
    app = setup_app()

    container = container or setup_container()
    fastapi.setup_dishka(container=container, app=app)

    return cast(FastAPIContainerized, app)

