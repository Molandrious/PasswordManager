from dishka import FromDishka
from faststream.rabbit import RabbitRouter
from src.databases.sqlalchemy.orm import EventORM
from src.integrations.faststream.rabbit import RabbitQueues
from src.models.event import EventType
from src.repositories import EventRepository
from src.transport.rabbit.event_topic.schemas import CreateEventResponse, CreateEventSchema

rabbit_mq_router = RabbitRouter()


@rabbit_mq_router.subscriber(RabbitQueues.event)
async def create_event_rabbit_handler(
    message: CreateEventSchema,
    event_repository: FromDishka[EventRepository],
):
    event_id = await event_repository.create(EventORM(message=message.message, type=EventType.manual))
    return CreateEventResponse(event_id=event_id)
