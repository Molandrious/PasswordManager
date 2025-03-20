from faststream.rabbit import RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter
from loguru import logger

from src.settings import get_settings


class RabbitQueues:
    event = RabbitQueue(name='event')


rabbit_mq_broker = RabbitRouter(
    url=get_settings().env.rabbit.dsn.unicode_string(),
    # logger=logger,
)
