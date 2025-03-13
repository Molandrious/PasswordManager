from dishka import FromDishka
from starlette import status

from src.errors import ObjectNotFoundError
from src.services import PasswordService
from src.transport.rest import errors
from src.transport.rest.routers.password.schemas import (
    CreatePasswordPayload,
    GetPasswordResponse,
    SearchPasswordsResponse,
)
from src.transport.rest.utils import DishkaAPIRouter

password_router = DishkaAPIRouter(prefix='/password', tags=['password'])


@password_router.post(
    '/{service_name}',
    status_code=status.HTTP_201_CREATED,
)
async def create_service_password_handler(
    password_service: FromDishka[PasswordService],
    service_name: str,
    payload: CreatePasswordPayload,
) -> None:
    await password_service.create_password_for_service(service_name=service_name, password=payload.password)


@password_router.get(
    '/{service_name}',
    response_model=GetPasswordResponse,
)
async def get_service_password_handler(
    password_service: FromDishka[PasswordService],
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
async def search_services_passwords_handler(
    password_service: FromDishka[PasswordService],
    service_name: str,
) -> SearchPasswordsResponse:
    result = await password_service.search_services_passwords(service_name=service_name)

    return SearchPasswordsResponse.model_validate({'items': result})
