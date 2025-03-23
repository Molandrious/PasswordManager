from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import cast

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_ioc
from dishka.integrations.faststream import setup_dishka as setup_faststream_ioc
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger

from src.ios.setup import setup_ios_container
from src.integrations.faststream.kafka import kafka_broker
from src.integrations.faststream.rabbit import rabbit_router
from src.integrations.taskiq.broker import taskiq_broker
from src.logger import AppLogger
from src.settings import get_settings
from src.transport.kafka.event_topic.handlers import kafka_router
from src.transport.rabbit.event_topic.handlers import rabbit_mq_router
from src.transport.rest import FastAPIContainerized
from src.transport.rest.setup import setup_error_handlers, setup_middlewares, setup_routers


@asynccontextmanager
async def lifespan(
    app: FastAPIContainerized,
) -> AsyncGenerator[None]:
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
    rabbit_router.include_router(rabbit_mq_router)
    app.include_router(rabbit_router)
    setup_faststream_ioc(container, rabbit_router, auto_inject=True, finalize_container=False)


def setup_kafka(app: FastAPI, container: AsyncContainer) -> None:
    kafka_broker.include_router(kafka_router)
    app.include_router(kafka_broker)
    setup_faststream_ioc(container, kafka_broker, auto_inject=True, finalize_container=False)


def make_app(
    container: AsyncContainer | None = None,
) -> FastAPIContainerized:
    app = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
        logger=logger,
    )

    AppLogger.make()
    container = container or setup_ios_container(settings=get_settings())

    setup_rest(app=app, container=container)
    setup_rabbit(app=app, container=container)
    # setup_kafka(app=app, ios=ios)

    return cast(FastAPIContainerized, app)

