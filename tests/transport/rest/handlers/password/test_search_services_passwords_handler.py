from functools import partial

import pytest
from httpx import AsyncClient
from starlette import status

from src.transport.rest import FastAPIContainerized
from src.transport.rest.routers.password.handlers import search_services_passwords_handler
from tests.factories import ServicePasswordFactory


@pytest.mark.require_db
class TestSearchServicesPasswordsHandler:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        app: FastAPIContainerized,
        test_client: AsyncClient,
    ) -> None:
        self.client = test_client
        self.url = partial(app.url_path_for, search_services_passwords_handler.__name__)

    async def test_ok(self, service_password_factory: ServicePasswordFactory) -> None:
        search_part = 'some_'

        await service_password_factory.create_async(service_name=f'{search_part}service')
        await service_password_factory.create_async(service_name=f'{search_part}service_2')
        await service_password_factory.create_async(service_name='another_service')

        response = await self.client.get(url=self.url(), params={'service_name': search_part})

        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response.json()['items']) == 2

    async def test_empty(
        self,
    ) -> None:
        response = await self.client.get(url=self.url(), params={'service_name': 'search_part'})

        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response.json()['items']) == 0
