from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.databases.sqlalchemy.orm.base import BaseORM
from src.models.event import Event, EventType


class EventORM(BaseORM):
    __entity__ = Event

    message: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[EventType] = mapped_column(String, nullable=False)
