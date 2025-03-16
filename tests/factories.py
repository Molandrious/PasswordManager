from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from polyfactory.pytest_plugin import register_fixture

from src.databases.sqlalchemy.orm import PasswordORM
from src.services.password.utils import EncryptUtils
from src.settings import get_settings


@register_fixture
class ServicePasswordFactory(SQLAlchemyFactory[PasswordORM]):
    @classmethod
    def hashed_password(cls) -> bytes:
        return EncryptUtils(get_settings().env.secret_key).encrypt_password(cls.__faker__.password())
