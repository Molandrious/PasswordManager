from src.databases.sqlalchemy.orm import EventORM

from src.models.event import Event
from src.packages.sql_aclhemy_utils.repository import ISqlAlchemyRepository


class EventRepository(ISqlAlchemyRepository[EventORM, Event]):
    _orm = EventORM
    _entity = Event
    _orm_search_fields = [EventORM.message]
