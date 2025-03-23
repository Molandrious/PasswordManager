
from granian.constants import Interfaces

from src.bootstrap import make_app  # noqa
from src.settings import ASGIProvider, get_settings


def main() -> None:
    settings = get_settings()

    if settings.env.asgi_provider == ASGIProvider.GRANIAN:
        from granian import Granian
        Granian(
            'main:make_app',
            address=settings.env.rest.host,
            port=settings.env.rest.port,
            interface=Interfaces.ASGI,
            factory=True,
        ).serve()
    elif settings.env.asgi_provider == ASGIProvider.UVICORN:
        import uvicorn
        uvicorn.run(
            app='main:make_app',
            host=settings.env.rest.host,
            port=settings.env.rest.port,
            factory=True,
            workers=1,
        )


if __name__ == '__main__':
    main()
