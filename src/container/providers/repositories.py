from dishka import FromDishka, provide, Provider, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories import EventRepository, PasswordRepository


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    @provide()
    def password_repository(self, session: FromDishka[AsyncSession]) -> PasswordRepository:
        return PasswordRepository(session=session)

    @provide()
    def event_repository(self, session: FromDishka[AsyncSession]) -> EventRepository:
        return EventRepository(session=session)
