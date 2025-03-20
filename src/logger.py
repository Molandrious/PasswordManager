import logging
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from loguru import logger
from loguru._defaults import LOGURU_FORMAT
from loguru._recattrs import RecordLevel

from src.settings import Settings

LOGLEVEL_MAPPING = {
    50: 'CRITICAL',
    40: 'ERROR',
    30: 'WARNING',
    20: 'INFO',
    11: 'DB_ECHO',
    10: 'DEBUG',
    0: 'NOTSET',
}

class InnerAppLogsHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = LOGLEVEL_MAPPING.get(record.levelno, 'NOTSET')

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(
            request_id='app',
            method=record.funcName,
            file=record.filename,
            name=record.name,
        )
        log.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def custom_time(*_args):
    return datetime.now(tz=ZoneInfo('Europe/Moscow'))


class AppLogger:
    format: str = LOGURU_FORMAT

    @classmethod
    def make(cls):
        settings = Settings()

        logger.remove()

        logger.add(
            sys.stderr,
            level=settings.env.logger.level.upper(),
            catch=True,
            enqueue=True,
            backtrace=True,
            format=cls.custom_formatter,
            filter=cls.log_message_filter,
        )

        if settings.env.logger.path:
            logger.add(
                settings.env.logger.path,
                catch=True,
                enqueue=True,
                backtrace=True,
                delay=True,
                serialize=True,
            )

        for logger_title in [
            '_granian',
            'granian.access',
            'fastapi',
            'sqlalchemy.engine.Engine',
        ]:
            _logger = logging.getLogger(logger_title)
            _logger.handlers = [InnerAppLogsHandler()]

        logger.info(logging.Logger.manager.loggerDict)

        for logger_title in []:
            _logger = logging.getLogger(logger_title)
            _logger.handlers = []

        return logger.bind(request_id=None, method=None, file=None, name=None)

    @staticmethod
    def custom_formatter(record: dict) -> str:
        custom_format = AppLogger.format + '\n'
        record['time'] = datetime.astimezone(record['time'], ZoneInfo('Europe/Moscow'))

        if record['extra'].get('name') == 'sqlalchemy.engine.Engine':
            record['level'] = RecordLevel(name='DB_ECHO', no=11, icon='🔵')
            custom_format = custom_format.replace('cyan', 'fg #FFA500')
            custom_format = custom_format.replace(
                '<level>{level: <8}</level>',
                AppLogger.wrap_str_in_color(string='<level>{level: <8}</level>', color='fg #FFA500'),
            )
        return custom_format

    @staticmethod
    def wrap_str_in_color(string: str, color: str) -> str:
        return f'<{color}>{string}</{color}>'

    @staticmethod
    def log_message_filter(record: dict) -> bool:
        if record['extra'].get('name') == 'sqlalchemy.engine.Engine' and record['message'] == '[raw sql] ()':
            return False

        if 'GET /metrics' in record['message']:
            return False

        return True
