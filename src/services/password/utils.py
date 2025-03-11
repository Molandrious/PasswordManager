from attrs import define
from cryptography.fernet import Fernet
from pydantic import SecretBytes

@define
class EncryptUtils:
    secret_key: SecretBytes

    def encrypt_password(self, password: str) -> bytes:
        fernet = Fernet(self.secret_key.get_secret_value())
        return fernet.encrypt(password.encode())

    def decrypt_password(self, encrypted_password: bytes) -> str:
        fernet = Fernet(self.secret_key.get_secret_value())
        return fernet.decrypt(encrypted_password).decode()


