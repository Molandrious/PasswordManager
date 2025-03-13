from functools import partial

import pytest
from dishka import Scope
from httpx import AsyncClient
from starlette import status

from src.repositories import PasswordRepository
from src.transport.rest import FastAPIContainerized
from src.transport.rest.routers.password.handlers import get_service_password_handler
from tests.factories import ServicePasswordFactory


@pytest.mark.require_db
class TestCreateServicePasswordHandler:
    @pytest.fixture(autouse=True)
    async def setup(
        self,
        app: FastAPIContainerized,
        test_client: AsyncClient,
    ) -> None:
        self.client = test_client
        self.url = partial(app.url_path_for, get_service_password_handler.__name__)
        async with app.state.dishka_container(scope=Scope.REQUEST) as request_container:
            self.password_repository = await request_container.get(PasswordRepository)

    async def test_new(self) -> None:
        service_name = 'some_service'
        password = 'some_password'

        response = await self.client.post(url=self.url(service_name=service_name), json={'password': password})

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

        db_object = await self.password_repository.get_one_by(service_name=service_password.service_name)

        assert db_object.hashed_password != service_password.hashed_password
