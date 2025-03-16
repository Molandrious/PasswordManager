from dishka.integrations import taskiq
from taskiq import InMemoryBroker, TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

from src.container.setup import setup_container
from src.settings import Environment, get_settings

_settings = get_settings()

if _settings.env.environment == Environment.TESTS:
    broker = InMemoryBroker()
else:
    result_backend = RedisAsyncResultBackend(redis_url=_settings.env.redis.dsn.unicode_string())

    broker = RedisStreamBroker(
        url=_settings.env.redis.dsn.unicode_string(),
        timeout=2,
    ).with_result_backend(result_backend)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)

taskiq.setup_dishka(container=setup_container(_settings), broker=broker)





