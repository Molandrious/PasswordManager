from faststream.kafka.fastapi import KafkaRouter

from src.integrations.faststream.logger import fast_stream_logger
from src.settings import get_settings


class KafkaTopics:
    event = 'event'


kafka_broker = KafkaRouter(
    bootstrap_servers=get_settings().env.kafka.dsn.unicode_string(),
    logger=fast_stream_logger,
)
