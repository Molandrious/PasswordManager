import contextlib
from collections.abc import AsyncGenerator

from starlette.requests import Request


async def clear_container_resources_depends(
    request: Request,
) -> AsyncGenerator[None, None]:
    try:
        yield
    finally:
        with contextlib.suppress(TypeError):
            await request.app.container.shutdown_resources()
