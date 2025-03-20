from dishka.integrations import taskiq
from taskiq import InMemoryBroker, TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

from src.container.setup import setup_container
from src.settings import Environment, get_settings


def setup_taskiq_broker():
    settings = get_settings()

    if settings.env.environment == Environment.TESTS:
        broker = InMemoryBroker()
    else:
        result_backend = RedisAsyncResultBackend(redis_url=settings.env.redis.dsn.unicode_string())

        broker = RedisStreamBroker(
            url=settings.env.redis.dsn.unicode_string(),
        ).with_result_backend(result_backend)

    taskiq.setup_dishka(container=setup_container(settings), broker=broker)

    return broker


taskiq_broker = setup_taskiq_broker()
taskiq_scheduler = TaskiqScheduler(
    broker=taskiq_broker,
    sources=[LabelScheduleSource(taskiq_broker)],
)

