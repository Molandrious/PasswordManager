from src.packages.common.models import ConfiguredBaseModel


class DecryptedServicePasswordDTO(ConfiguredBaseModel):
    service_name: str
    password: str
