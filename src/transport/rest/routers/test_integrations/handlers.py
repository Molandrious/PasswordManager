from dishka import FromDishka
from faststream.kafka import KafkaBroker
from faststream.rabbit import RabbitBroker
from starlette import status

from src.integrations.faststream.kafka import KafkaTopics
from src.integrations.faststream.rabbit import RabbitQueues
from src.integrations.taskiq.worker_tasks import add_one_task, create_event_task
from src.transport.rabbit.event_topic.schemas import CreateEventSchema
from src.transport.rest.utils import DishkaAPIRouter

test_integrations = DishkaAPIRouter(prefix='/integrations', tags=['integrations'])


@test_integrations.post(
    '/taskiq',
    status_code=status.HTTP_201_CREATED,
)
async def create_event_taskiq_handler() -> None:
    task = await create_event_task.kiq()
    return task.task_id


@test_integrations.get(
    '/taskiq',
    status_code=status.HTTP_200_OK,
)
async def search_services_passwords_handler() -> None:
    task = await add_one_task.kiq(10)
    return await task.wait_result()


@test_integrations.post(
    '/faststream/rabbit',
    status_code=status.HTTP_200_OK,
)
async def push_message_to_faststream_rabbit_topic_handler(message: str, rabbit: FromDishka[RabbitBroker]):
    id = await rabbit.publish(CreateEventSchema(message=message), queue=RabbitQueues.event)
    return {'id': id}


@test_integrations.post(
    '/faststream/kafka',
    status_code=status.HTTP_200_OK,
)
async def push_message_to_kafka_topic_handler(message: str, kafka: FromDishka[KafkaBroker]):
    id = await kafka.publish(CreateEventSchema(message=message), topic=KafkaTopics.event)
    return {'id': id}
