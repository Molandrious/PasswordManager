from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import src
from src.containers.app import App
from src.transport.rest.setup_entrypoints import init_endpoints, init_middlewares
from src.transport.rest.setup_errors import init_fastapi_error_handlers


class FastAPIContainerized(FastAPI):
    container: App


@asynccontextmanager
async def _lifespan(
    app: FastAPI,  # noqa
) -> AsyncGenerator[None]:
    yield


def make_app() -> FastAPIContainerized:
    app = FastAPIContainerized(
        lifespan=_lifespan,
        default_response_class=ORJSONResponse,
    )

    app.container = App()
    app.container.wire(packages=[src.transport.rest])

    init_endpoints(app)
    init_middlewares(app)
    init_fastapi_error_handlers(app)

    return app
