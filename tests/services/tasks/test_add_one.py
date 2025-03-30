import pytest
from dishka import Scope

from src.services.tasks.add_one import AddOneTask
from src.transport.rest import FastAPIContainerized


class TestAddOne:
    @pytest.fixture(autouse=True)
    async def setup(self, app: FastAPIContainerized):
        async with app.state.dishka_container(scope=Scope.REQUEST) as request_container:
            self.task = await request_container.get(AddOneTask)

    async def test_ok(self):
        assert await self.task(10) == 11
