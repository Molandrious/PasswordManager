from enum import auto, StrEnum

from src.packages.common.models import EntityModel


class EventType(StrEnum):
    manual = auto()
    scheduled = auto()


class Event(EntityModel):
    message: str
    type: EventType
