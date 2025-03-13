from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from polyfactory.pytest_plugin import register_fixture
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.databases.postgres.orm import PasswordORM
from src.services.password.utils import EncryptUtils
from src.settings import get_settings

FactoryAsyncSession = async_sessionmaker()
SQLAlchemyFactory.__async_session__ = FactoryAsyncSession


@register_fixture
class ServicePasswordFactory(SQLAlchemyFactory[PasswordORM]):
    @classmethod
    def hashed_password(cls) -> bytes:
        return EncryptUtils(get_settings().env.secret_key).encrypt_password(cls.__faker__.password())
