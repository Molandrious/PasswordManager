from attrs import define
from pydantic import SecretBytes

from src.databases.postgres.orm.password import PasswordORM
from src.errors import ObjectNotFoundError
from src.repositories.password import PasswordRepository
from src.services.password.dto import DecryptedServicePasswordDTO
from src.services.password.utils import EncryptUtils


@define
class PasswordService(EncryptUtils):
    password_repository: PasswordRepository
    secret_key: SecretBytes

    async def create_password_for_service(self, service_name: str, password: str) -> None:
        hashed_password = self.encrypt_password(password=password)

        service_password = await self.password_repository.get_one_by(service_name=service_name)

        if not service_password:
            await self.password_repository.create(
                PasswordORM(service_name=service_name, hashed_password=hashed_password)
            )
        else:
            await self.password_repository.update_object(
                PasswordORM(id=service_password.id, service_name=service_name, hashed_password=hashed_password)
            )

    async def get_service_password(self, service_name: str) -> DecryptedServicePasswordDTO:
        service_password = await self.password_repository.get_one_by(service_name=service_name)

        if not service_password:
            raise ObjectNotFoundError

        return DecryptedServicePasswordDTO(
            service_name=service_password.service_name,
            password=self.decrypt_password(service_password.hashed_password),
        )

    async def search_services_passwords(self, service_name: str) -> list[DecryptedServicePasswordDTO]:
        service_password_list = await self.password_repository.get_list(search=service_name)

        return [
            DecryptedServicePasswordDTO(
                service_name=service_password.service_name,
                password=self.decrypt_password(service_password.hashed_password),
            )
            for service_password in service_password_list
        ]
