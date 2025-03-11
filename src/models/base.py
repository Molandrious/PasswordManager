from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )


class BaseEntity(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID


class CreateAndUpdateAtMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
