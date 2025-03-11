from dependency_injector.wiring import inject
from fastapi import APIRouter
from starlette import status

from src.errors import ObjectNotFoundError
from src.transport.rest import errors
from src.transport.rest.annotations import PasswordServiceAnnotated
from src.transport.rest.routers.password.schemas import (
    CreatePasswordPayload,
    GetPasswordResponse,
    SearchPasswordsResponse,
)

password_router = APIRouter(prefix='/password', tags=['password'])


@password_router.post(
    '/{service_name}',
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_service_password_handler(
    password_service: PasswordServiceAnnotated,
    service_name: str,
    payload: CreatePasswordPayload,
) -> None:
    await password_service.create_password_for_service(service_name=service_name, password=payload.password)


@password_router.get(
    '/{service_name}',
    response_model=GetPasswordResponse,
)
@inject
async def get_service_password_handler(
    password_service: PasswordServiceAnnotated,
    service_name: str,
) -> GetPasswordResponse:
    try:
        result = await password_service.get_service_password(service_name=service_name)
    except ObjectNotFoundError as err:
        raise errors.ObjectNotFoundError from err

    return GetPasswordResponse.model_validate(result)


@password_router.get(
    '/',
    response_model=SearchPasswordsResponse,
)
@inject
async def search_services_passwords_handler(
    password_service: PasswordServiceAnnotated,
    service_name: str,
) -> SearchPasswordsResponse:
    result = await password_service.search_services_passwords(service_name=service_name)

    return SearchPasswordsResponse.model_validate({'items': result})
