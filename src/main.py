from granian import Granian
from granian.constants import Interfaces

from src.bootstrap import make_app  # noqa
from src.settings import get_settings


def main() -> None:
    settings = get_settings()

    Granian(
        'main:make_app',
        address=settings.env.rest.host,
        port=settings.env.rest.port,
        interface=Interfaces.ASGI,
        factory=True,
    ).serve()


if __name__ == '__main__':
    main()
