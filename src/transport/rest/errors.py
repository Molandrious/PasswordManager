from starlette import status


class ServerError(Exception):
    status_code: int = 520
    message: str = 'Something went wrong'

    @property
    def title(self) -> str:
        return self.__class__.__name__

    def __init__(
        self,
        message: str | None = None,
    ):
        self.message = message or self.message
        super().__init__()

    def as_dict(self) -> dict:
        return {
            'title': self.title,
            'message': self.message,
        }


class ObjectNotFoundError(ServerError):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Object not found'
