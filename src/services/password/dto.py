from src.models.base import BaseDTO


class DecryptedServicePasswordDTO(BaseDTO):
    service_name: str
    password: str
