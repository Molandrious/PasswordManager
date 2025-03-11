from traceback import print_exc

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from src.transport.rest.errors import ServerError
from src.transport.rest.setup_errors import process_server_error


class ErrorsHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        try:
            return await call_next(request)
        except ServerError as exc:
            return process_server_error(
                request=request,
                exc=exc,
            )
        except Exception:
            print_exc()

            return process_server_error(
                request=request,
                exc=ServerError(),
            )
