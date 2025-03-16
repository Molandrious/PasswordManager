from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import cast

from dishka import AsyncContainer
from dishka.integrations import fastapi
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.container.setup import setup_container
from src.settings import get_settings
from src.transport.rest import FastAPIContainerized
from src.transport.rest.setup import setup_error_handlers, setup_middlewares, setup_routers
from transport.taskiq.broker import broker


@asynccontextmanager
async def lifespan(
    app: FastAPIContainerized,
) -> AsyncGenerator[None]:
    await broker.startup()

    yield

    await broker.shutdown()

    await app.state.dishka_container.close()


def setup_rest_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse, redirect_slashes=False)

    setup_routers(app)
    setup_middlewares(app)
    setup_error_handlers(app)

    return app


def make_app(
    container: AsyncContainer | None = None,
) -> FastAPIContainerized:
    app = setup_rest_app()

    container = container or setup_container(settings=get_settings())

    fastapi.setup_dishka(container=container, app=app)

    return cast(FastAPIContainerized, app)

