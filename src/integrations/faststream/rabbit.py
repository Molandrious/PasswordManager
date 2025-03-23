from faststream.rabbit import RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter
from src.integrations.faststream.logger import FastStreamLogger
from src.settings import get_settings


class RabbitQueues:
    event = RabbitQueue(name='event')


rabbit_router = RabbitRouter(
    url=get_settings().env.rabbit.dsn.unicode_string(),
    logger=FastStreamLogger(),
)
