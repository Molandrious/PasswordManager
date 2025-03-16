from starlette import status

from src.transport.rest.utils import DishkaAPIRouter
from src.transport.taskiq.tasks import create_event_task, simple_task

event_router = DishkaAPIRouter(prefix='/event', tags=['event'])


@event_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
)
async def create_event_handler() -> None:
    task = await create_event_task.kiq()
    return task.task_id


@event_router.get(
    '/',
    status_code=status.HTTP_200_OK,
)
async def get_value_from_task_handler() -> None:
    task = await simple_task.kiq(10)
    return await task.wait_result()
