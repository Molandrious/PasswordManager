from dishka import FromDishka, provide, Provider, Scope

from src.repositories import PasswordRepository
from src.services import PasswordService
from src.settings import Settings


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.REQUEST)
    def password_service(
        self,
        password_repository: FromDishka[PasswordRepository],
        settings: FromDishka[Settings],
    ) -> PasswordService:
        return PasswordService(password_repository, settings.env.secret_key)
