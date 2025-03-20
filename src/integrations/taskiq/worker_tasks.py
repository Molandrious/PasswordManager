from uuid import UUID

from dishka import FromDishka
from dishka.integrations.taskiq import inject

from src.integrations.taskiq.broker import taskiq_broker
from src.services.tasks.add_one import AddOneTask
from src.services.tasks.create_event import CreateEventTask


@taskiq_broker.task(task_name='add_one_task')
async def add_one_task(add_one: FromDishka[AddOneTask], value: int) -> int:
    return await add_one(value)


@taskiq_broker.task(task_name='create_event_task')
@inject
async def create_event_task(create_event: FromDishka[CreateEventTask], message: str) -> UUID:
    return await create_event(message)
