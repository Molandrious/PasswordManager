from src.transport.rest.base_schema import BaseApiSchema


class CreatePasswordPayload(BaseApiSchema):
    password: str


class GetPasswordResponse(BaseApiSchema):
    service_name: str
    password: str


class SearchPasswordsResponse(BaseApiSchema):
    items: list[GetPasswordResponse]
