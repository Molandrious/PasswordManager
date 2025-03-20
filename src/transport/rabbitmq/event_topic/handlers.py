from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import RabbitRouter

from src.databases.sqlalchemy.orm import EventORM
from src.integrations.faststream.rabbit_mq import RabbitQueues
from src.models.event import EventType
from src.repositories import EventRepository
from src.transport.rabbitmq.event_topic.schemas import CreateEventSchema

rabbit_mq_router = RabbitRouter()


@rabbit_mq_router.subscriber(RabbitQueues.event)
@rabbit_mq_router.publisher('response')
@inject
async def create_event_handler(
    message: CreateEventSchema,
    event_repository: FromDishka[EventRepository],
):
    event_id = await event_repository.create(EventORM(message=message.message, type=EventType.manual))
    return {'response': event_id}
