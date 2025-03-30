from functools import partial

import pytest
from dishka import Scope
from httpx import AsyncClient
from src.repositories import PasswordRepository
from src.transport.rabbit.event_topic.handlers import create_event_rabbit_handler
from src.transport.rest import FastAPIContainerized
from src.transport.rest.routers.password.handlers import (
    create_service_password_handler,
    get_service_password_handler,
    search_services_passwords_handler,
)
from starlette import status
from tests.factories import ServicePasswordFactory


@pytest.mark.require_db()
class TestCreateServicePasswordHandler:
    @pytest.fixture(autouse=True)
    async def setup(
        self,
        app: FastAPIContainerized,
        test_client: AsyncClient,
    ) -> None:
        self.client = test_client
        self.url = partial(app.url_path_for, create_service_password_handler.__name__)
        async with app.state.dishka_container(scope=Scope.REQUEST) as request_container:
            self.password_repository = await request_container.get(PasswordRepository)

    async def test_new(self) -> None:
        service_name = 'some_service'
        password = 'some_password'

        response = await self.client.post(url=self.url(service_name=service_name), json={'password': password})

        create_event_rabbit_handler.mock.assert_called_once_with({'message': f'Password created for {service_name}'})
        assert response.status_code == status.HTTP_201_CREATED, response.text
        assert await self.password_repository.get_one_by(service_name=service_name) is not None

    async def test_with_update(
        self,
        service_password_factory: ServicePasswordFactory,
    ) -> None:
        service_password = await service_password_factory.create_async()

        response = await self.client.post(
            url=self.url(service_name=service_password.service_name), json={'password': 'new_password'}
        )

        assert response.status_code == status.HTTP_201_CREATED, response.text
        create_event_rabbit_handler.mock.assert_called_once_with(
            {'message': f'Password created for {service_password.service_name}'}
        )

        db_object = await self.password_repository.get_one_by(service_name=service_password.service_name)
        assert db_object.hashed_password != service_password.hashed_password


@pytest.mark.require_db()
class TestGetServicePasswordHandler:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        app: FastAPIContainerized,
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


@pytest.mark.require_db()
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
        assert len(response.json()['items']) == 2, response.text

    async def test_empty(
        self,
    ) -> None:
        response = await self.client.get(url=self.url(), params={'service_name': 'search_part'})

        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response.json()['items']) == 0
