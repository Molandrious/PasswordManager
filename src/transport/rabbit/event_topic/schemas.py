from uuid import UUID

from pydantic import BaseModel


class CreateEventSchema(BaseModel):
    message: str


class CreateEventResponse(BaseModel):
    event_id: UUID
