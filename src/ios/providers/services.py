from dishka import FromDishka, provide, Provider, Scope

from src.repositories import EventRepository, PasswordRepository
from src.services import PasswordService
from src.services.tasks.add_one import AddOneTask
from src.services.tasks.create_event import CreateEventTask
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

    @provide()
    def add_one_task(self) -> AddOneTask:
        return AddOneTask()

    @provide()
    def create_event_task(self, event_repository: FromDishka[EventRepository]) -> CreateEventTask:
        return CreateEventTask(event_repository=event_repository)
