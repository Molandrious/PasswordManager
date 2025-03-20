from loguru import logger


class AddOneTask:
    async def __call__(self, value: int) -> int:
        logger.info('Task add_one_task started')
        return value + 1

