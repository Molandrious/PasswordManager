from typing import Any

from faststream.types import LoggerProto
from loguru import logger
from src.logger import LOGLEVEL_MAPPING


class FastStreamLogger(LoggerProto):
    @classmethod
    def log(
        cls,
        level: int,
        msg: Any,
        exc_info: Any | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        level = LOGLEVEL_MAPPING.get(level, level)
        _extra = ':'.join(v for v in extra.values() if v)
        logger.log(level, msg, faststream=_extra, exc_info=exc_info)


fast_stream_logger = FastStreamLogger
