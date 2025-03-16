from src.packages.common.models import EntityModel


class ServicePassword(EntityModel):
    service_name: str
    hashed_password: bytes
