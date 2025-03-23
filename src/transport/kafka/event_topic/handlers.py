from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.kafka import KafkaRouter
from src.databases.sqlalchemy.orm import EventORM
from src.integrations.faststream.kafka import KafkaTopics
from src.models.event import EventType
from src.repositories import EventRepository
from src.transport.rabbit.event_topic.schemas import CreateEventSchema

kafka_router = KafkaRouter()


@kafka_router.subscriber(KafkaTopics.event)
@inject
async def create_event_kafka_handler(
    message: CreateEventSchema,
    event_repository: FromDishka[EventRepository],
):
    event_id = await event_repository.create(EventORM(message=message.message, type=EventType.manual))
    return {'response': event_id}
