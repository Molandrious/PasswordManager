from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseApiSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )
