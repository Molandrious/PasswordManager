import pytest
from faststream.rabbit import RabbitBroker, RabbitQueue
from src.integrations.faststream.rabbit import RabbitQueues
from src.repositories import EventRepository
from src.transport.rabbit.event_topic.schemas import CreateEventResponse


@pytest.mark.require_db()
class TestCreateEventRabbitHandler:
    queue: RabbitQueue = RabbitQueues.event

    async def test_ok(self, rabbit_broker: RabbitBroker, event_repository: EventRepository):
        response = await rabbit_broker.request({'message': 'SomeTest'}, queue=self.queue)

        assert response.body, response

        response_body = CreateEventResponse.model_validate_json(response.body)
        assert await event_repository.get_one_by(id=response_body.event_id)
