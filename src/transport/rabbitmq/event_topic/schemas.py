from pydantic import BaseModel


class CreateEventSchema(BaseModel):
    message: str
