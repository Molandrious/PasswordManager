import asyncio
import sys
from asyncio import AbstractEventLoop
from collections.abc import Generator
from typing import Any, AsyncGenerator

import psycopg2
import pytest
from alembic import command
from alembic.config import Config
from dishka import AsyncContainer
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from loguru import logger
from pytest_docker.plugin import get_docker_services
from sqlalchemy.ext.asyncio import create_async_engine

from src.bootstrap import FastAPIContainerized, make_app, setup_container
from src.databases.postgres.client import SQLAlchemyClient
from src.settings import Settings
from tests.factories import FactoryAsyncSession


def pytest_configure(config):  # noqa
    settings = Settings()
    if settings.env.tests.create_docker_postgres_for_tests:
        settings.env.postgres.dsn = settings.env.tests.docker_test_db_dsn
    else:
        settings.env.postgres.dsn = settings.env.tests.local_test_db_dsn

    FactoryAsyncSession.configure(bind=create_async_engine(url=settings.env.postgres.dsn.unicode_string()))


@pytest.fixture(scope='session', autouse=True)
def anyio_backend(request):  # noqa
    return 'asyncio'


@pytest.fixture(scope='session', autouse=True)
def event_loop() -> Generator[AbstractEventLoop, Any, None]:
    logger.debug('Setting event loop')
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()

    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def settings() -> Settings:
    settings = Settings()

    if settings.env.tests.create_docker_postgres_for_tests:
        settings.env.postgres.dsn = settings.env.tests.docker_test_db_dsn
    else:
        settings.env.postgres.dsn = settings.env.tests.local_test_db_dsn

    return settings


@pytest.fixture(scope='session')
async def init_test_db_docker_container(
    docker_compose_command: str,
    docker_setup: str,
    docker_cleanup: str,
    settings: Settings,
    request: pytest.FixtureRequest,
) -> AsyncGenerator[bool, None]:
    is_docker_db_created = False

    if not settings.env.tests.create_docker_postgres_for_tests:
        logger.info('create_docker_postgres_for_tests is False. Skipping Docker database creation.')
        yield is_docker_db_created
        return

    if not any(item.get_closest_marker('require_db') for item in request.session.items):
        logger.info('No tests require a database. Skipping Docker database creation.')
        yield is_docker_db_created
        return

    docker_service_cm = get_docker_services(
        docker_compose_command,
        settings.root_path.joinpath('tests/docker-compose.yml'),
        'password_manager_tests_postgres',
        docker_setup,
        docker_cleanup,
    )

    def is_postgres_responsive() -> bool:
        try:
            dsn = settings.env.postgres.dsn.unicode_string().replace('postgresql+asyncpg', 'postgresql')
            conn = psycopg2.connect(dsn=dsn)
            conn.close()
        except Exception:  # noqa
            return False
        return True

    with docker_service_cm as docker_service:
        docker_service.wait_until_responsive(check=is_postgres_responsive, timeout=10, pause=1)  # noqa
        is_docker_db_created = True
        yield is_docker_db_created


@pytest.fixture(scope='session', autouse=True)
async def _do_migrations_for_test_db(
    init_test_db_docker_container: bool,  # noqa: FBT001
    settings: Settings,
) -> None:
    if not init_test_db_docker_container:
        return

    logger.debug('Applying database migrations...')
    alembic_cfg = Config(settings.root_path.joinpath('alembic.ini'))
    alembic_cfg.set_main_option('script_location', settings.root_path.joinpath('migrations').as_posix())
    alembic_cfg.set_main_option('sqlalchemy.url', settings.env.postgres.dsn.unicode_string())
    command.downgrade(alembic_cfg, 'base')
    command.upgrade(alembic_cfg, 'head')

    return


@pytest.fixture(name='container')
async def test_container(settings: Settings) -> AsyncGenerator[AsyncContainer, Any]:
    container = setup_container(settings=settings)
    yield container
    await container.close()


@pytest.fixture()
async def app(container: AsyncContainer) -> FastAPIContainerized:
    return make_app(container=container)


@pytest.fixture(autouse=True)
async def _create_tables(request: pytest.FixtureRequest, container: AsyncContainer) -> None:
    if not any(marker.name == 'require_db' for marker in request.node.iter_markers()):
        return

    db = await container.get(SQLAlchemyClient)

    await db.clear_all_tables()
    await db.create_all_tables()


@pytest.fixture()
async def test_client(app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client
