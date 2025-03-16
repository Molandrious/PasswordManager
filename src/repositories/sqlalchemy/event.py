from src.databases.sqlalchemy.orm import EventORM

from src.models.event import Event
from src.repositories.sqlalchemy.base import ISqlAlchemyRepository


class EventRepository(ISqlAlchemyRepository[EventORM, Event]):
    _model = EventORM
    _entity = Event
    _model_search_fields = [EventORM.message]
