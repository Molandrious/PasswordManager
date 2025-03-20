from uuid import UUID

from dishka import FromDishka
from dishka.integrations.taskiq import inject

from src.integrations.taskiq.broker import taskiq_broker
from src.services.tasks.create_event import CreateEventTask


@taskiq_broker.task(task_name='create_event_scheduled_task', schedule=[{'cron': '* * * * *'}])
@inject
async def create_event_scheduled_task(create_event: FromDishka[CreateEventTask], message: str) -> UUID:
    return await create_event(message)
