from src.databases.postgres.orm.password import PasswordORM
from src.models.service_password import ServicePassword
from src.repositories.base import ISqlAlchemyRepository


class PasswordRepository(ISqlAlchemyRepository[PasswordORM, ServicePassword]):
    _model = PasswordORM
    _entity = ServicePassword
    _model_search_fields = [PasswordORM.service_name]


class PasswordRepository2(ISqlAlchemyRepository[PasswordORM, ServicePassword]):
    _model = PasswordORM
    _entity = ServicePassword
    _model_search_fields = [PasswordORM.service_name]
