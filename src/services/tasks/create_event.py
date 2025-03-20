from uuid import UUID

from attrs import define
from loguru import logger

from src.databases.sqlalchemy.orm import EventORM
from src.models.event import EventType
from src.repositories import EventRepository


@define
class CreateEventTask:
    event_repository: EventRepository

    async def __call__(self, message: str) -> UUID:
        logger.info('Task create_event_task started')
        return await self.event_repository.create(EventORM(message=message, type=EventType.manual))
