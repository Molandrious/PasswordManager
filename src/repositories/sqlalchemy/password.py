from src.databases.sqlalchemy.orm.password import PasswordORM
from src.models.service_password import ServicePassword
from src.packages.sql_aclhemy_utils.repository import ISqlAlchemyRepository


class PasswordRepository(ISqlAlchemyRepository[PasswordORM, ServicePassword]):
    _orm = PasswordORM
    _entity = ServicePassword
    _orm_search_fields = [PasswordORM.service_name]


class PasswordRepository2(ISqlAlchemyRepository[PasswordORM, ServicePassword]):
    _orm = PasswordORM
    _entity = ServicePassword
    _orm_search_fields = [PasswordORM.service_name]
