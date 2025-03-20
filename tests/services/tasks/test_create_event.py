import pytest
from dishka import Scope

from src.repositories import EventRepository
from src.services.tasks.create_event import CreateEventTask
from src.transport.rest import FastAPIContainerized


@pytest.mark.require_db
class TestCreateEvent:
    @pytest.fixture(autouse=True)
    async def setup(self, app: FastAPIContainerized):
        async with app.state.dishka_container(scope=Scope.REQUEST) as request_container:
            self.task = await request_container.get(CreateEventTask)
            self.event_repository = await request_container.get(EventRepository)

    async def test_ok(self):
        message = 'Test message'

        event_id = await self.task(message)
        event = await self.event_repository.get_one_by(id=event_id)

        assert event.message == message
