from dishka import provide, Provider, Scope

from src.settings import Settings


class CoreProvider(Provider):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings

    @provide(scope=Scope.APP)
    def settings_provider(self) -> Settings:
        return Settings()
