from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


class CamelCaseAliasModel(ConfiguredBaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class EntityModel(ConfiguredBaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
