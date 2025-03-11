from src.models.base import BaseEntity, CreateAndUpdateAtMixin


class ServicePassword(BaseEntity, CreateAndUpdateAtMixin):
    service_name: str
    hashed_password: bytes
