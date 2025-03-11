from functools import partial

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.transport.rest.errors import ServerError


def process_server_error(
    request: Request,  # noqa
    exc: ServerError,
) -> Response:
    response: JSONResponse = JSONResponse(
        content=exc.as_dict(),
        status_code=exc.status_code,
    )

    return response


def init_fastapi_error_handlers(
    app: FastAPI,
) -> None:
    app.add_exception_handler(
        exc_class_or_status_code=ServerError,
        handler=partial(process_server_error),
    )
