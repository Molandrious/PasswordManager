from src.packages.common.models import CamelCaseAliasModel


class CreatePasswordPayload(CamelCaseAliasModel):
    password: str


class GetPasswordResponse(CamelCaseAliasModel):
    service_name: str
    password: str


class SearchPasswordsResponse(CamelCaseAliasModel):
    items: list[GetPasswordResponse]
