from dishka import FromDishka, provide, Provider, Scope
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories import PasswordRepository
from src.repositories.password import PasswordRepository2


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    @provide()
    def password_repository(self, session: FromDishka[AsyncSession]) -> PasswordRepository:
        logger.info(f'Creating password repository with session {id(session)}')
        return PasswordRepository(session=session)

    @provide()
    def password_repository_2(self, session: FromDishka[AsyncSession]) -> PasswordRepository2:
        logger.info(f'Creating password repository 2 with session {id(session)}')
        return PasswordRepository2(session=session)
