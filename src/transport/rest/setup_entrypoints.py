from fastapi import APIRouter, FastAPI
from fastapi.params import Depends

from src.transport.rest.depends import clear_container_resources_depends
from src.transport.rest.middlewares.error_handler import ErrorsHandlerMiddleware
from src.transport.rest.routers.password.handlers import password_router


def init_endpoints(app: FastAPI) -> None:
    global_router = APIRouter(dependencies=[Depends(clear_container_resources_depends)])

    global_router.include_router(password_router)

    app.include_router(global_router)


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(ErrorsHandlerMiddleware)  # type: ignore
