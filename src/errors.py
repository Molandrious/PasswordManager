class BaseServiceError(Exception):
    message: str


class ObjectNotFoundError(BaseServiceError):
    message = 'Object not found'


class ObjectAlreadyExistsError(BaseServiceError):
    message = 'Object already exists'
