from dishka import FromDishka, make_async_container, provide, Provider, Scope
from dishka.integrations import fastapi
from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.faststream import inject, setup_dishka as setup_faststream_ioc
from fastapi import APIRouter, FastAPI
from faststream.rabbit.fastapi import RabbitRouter


class Postgres:
    async def some_func(self):
        print('some_func')


class GatewaysProvider(Provider):
    scope = Scope.APP

    @provide()
    def postgres(self) -> Postgres:
        return Postgres()


container = make_async_container(
    GatewaysProvider(),
)

mq_router = RabbitRouter(url='amqp://guest:guest@localhost:5672/')
http_router = APIRouter(route_class=DishkaRoute)


@mq_router.subscriber('test')
@inject
async def mq_handler(
    some_int: FromDishka[Postgres],
) -> None:
    await some_int.some_func()


@http_router.get('/')
async def http_handler(
    some_int: FromDishka[Postgres],
) -> str:
    await some_int.some_func()
    return 'Hello, FastAPI!'


def make_app():
    app = FastAPI()
    app.include_router(mq_router)
    app.include_router(http_router)

    setup_faststream_ioc(container, mq_router, finalize_container=False, auto_inject=True)
    fastapi.setup_dishka(container=container, app=app)

    return app


def main() -> None:
    import uvicorn

    uvicorn.run(
        app=make_app,
        host='127.0.0.1',
        port=8000,
        factory=True,
        workers=1,
    )



if __name__ == '__main__':
    main()
