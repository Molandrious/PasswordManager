from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import cast

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_ioc
from dishka.integrations.faststream import setup_dishka as setup_faststream_ioc
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger

from src.container.setup import setup_container
from src.integrations.faststream.rabbit_mq import rabbit_mq_broker
from src.integrations.taskiq.broker import taskiq_broker
from src.logger import AppLogger
from src.settings import get_settings
from src.transport.rabbitmq.event_topic.handlers import rabbit_mq_router
from src.transport.rest import FastAPIContainerized
from src.transport.rest.setup import setup_error_handlers, setup_middlewares, setup_routers


@asynccontextmanager
async def lifespan(
    app: FastAPIContainerized,
) -> AsyncGenerator[None]:
    logger.info('Lifespan')
    await taskiq_broker.startup()

    yield

    await taskiq_broker.shutdown()

    await app.state.dishka_container.close()


def setup_rest(app: FastAPI, container: AsyncContainer) -> None:
    setup_routers(app)
    setup_middlewares(app)
    setup_error_handlers(app)

    setup_fastapi_ioc(container, app)


def setup_rabbit(app: FastAPI, container: AsyncContainer) -> None:
    rabbit_mq_broker.include_router(rabbit_mq_router)

    app.include_router(rabbit_mq_broker)

    setup_faststream_ioc(container, rabbit_mq_broker, auto_inject=False, finalize_container=False)


def make_app(
    container: AsyncContainer | None = None,
) -> FastAPIContainerized:
    app = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
        logger=AppLogger.make(),
    )

    container = container or setup_container(settings=get_settings())

    setup_rest(app=app, container=container)
    setup_rabbit(app=app, container=container)

    print(logger)
    return cast(FastAPIContainerized, app)

