from functools import partial

from fastapi import FastAPI

from src.transport.rest.errors import ServerError
from src.transport.rest.middlewares.error_handler import ErrorsHandlerMiddleware
from src.transport.rest.routers.password.handlers import password_router
from src.transport.rest.utils import DishkaAPIRouter, process_server_error


def setup_routers(app: FastAPI) -> None:
    global_router = DishkaAPIRouter()

    global_router.include_router(password_router)

    app.include_router(global_router)


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(ErrorsHandlerMiddleware)  # type: ignore


def setup_error_handlers(
    app: FastAPI,
) -> None:
    app.add_exception_handler(
        exc_class_or_status_code=ServerError,
        handler=partial(process_server_error),
    )
