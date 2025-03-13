from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.transport.rest.errors import ServerError


class DishkaAPIRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('route_class'):
            kwargs['route_class'] = DishkaRoute

        super().__init__(*args, **kwargs)


def process_server_error(
    request: Request,  # noqa
    exc: ServerError,
) -> Response:
    response: JSONResponse = JSONResponse(
        content=exc.as_dict(),
        status_code=exc.status_code,
    )

    return response
