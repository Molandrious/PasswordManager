from functools import partial

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from src.transport.rest.routers.password.handlers import get_service_password_handler
from tests.factories import ServicePasswordFactory


@pytest.mark.require_db
class TestGetServicePasswordHandler:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        app: FastAPI,
        test_client: AsyncClient,
    ) -> None:
        self.client = test_client
        self.url = partial(app.url_path_for, get_service_password_handler.__name__)

    async def test_ok(self, service_password_factory: ServicePasswordFactory) -> None:
        password_service_orm = await service_password_factory.create_async()

        response = await self.client.get(url=self.url(service_name=password_service_orm.service_name))

        assert response.status_code == status.HTTP_200_OK, response.text

    async def test_not_found(
        self,
    ) -> None:
        response = await self.client.get(url=self.url(service_name='not_exist'))

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
