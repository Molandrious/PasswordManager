from uuid import UUID

from dishka import FromDishka
from dishka.integrations.taskiq import inject
from loguru import logger

from src.databases.sqlalchemy.orm import EventORM
from src.models.event import EventType
from src.repositories import EventRepository
from src.transport.taskiq.broker import broker


@broker.task(task_name='simple_task')
async def simple_task(value: int) -> int:
    logger.info('Task simple_task started')
    return value + 1


@broker.task(task_name='create_event_task')
@inject
async def create_event_task(event_repository: FromDishka[EventRepository]) -> bool:
    logger.info('Task create_event_task started')
    await event_repository.create(EventORM(message='Value', type=EventType.manual))
    return True


@broker.task(task_name='create_event_scheduled_task', schedule=[{'cron': '* * * * *'}])
@inject
async def create_event_scheduled_task(event_repository: FromDishka[EventRepository]) -> UUID:
    logger.info('Task create_event_task started')
    event_id = await event_repository.create(EventORM(message='Value', type=EventType.scheduled))
    return event_id

