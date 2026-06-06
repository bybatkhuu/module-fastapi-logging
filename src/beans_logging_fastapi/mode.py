import sys
from typing import TYPE_CHECKING

from pydantic import validate_call
from fastapi.concurrency import run_in_threadpool

if TYPE_CHECKING:
    from loguru import Logger
else:
    from loguru._logger import Logger

from potato_util.constants import WarnEnum
from beans_logging.constants import LogLevelEnum
from beans_logging import logger


@validate_call(config={"arbitrary_types_allowed": True})
async def async_log_at(
    message: str,
    level: LogLevelEnum | str = LogLevelEnum.INFO,
    warn_mode: WarnEnum | str = WarnEnum.ALWAYS,
    logger: Logger = logger,
) -> None:
    """Log message with level and warn mode in async context.

    Args:
        message   (str               , required): Message to log.
        level     (LogLevelEnum | str, optional): Log level when warn mode is `WarnEnum.ALWAYS`.
                                                    Defaults to `LogLevelEnum.INFO`.
        warn_mode (WarnEnum | str    , optional): Warn mode to use. Defaults to `WarnEnum.ALWAYS`.
        logger    (Logger            , optional): Logger instance to use. Defaults to `logger`.

    Raises:
        ValueError: If `level` is not a valid log level.
        ValueError: If `warn_mode` is not a valid warn mode.
    """

    if isinstance(level, str):
        level = LogLevelEnum(level.strip().upper())

    if isinstance(warn_mode, str):
        warn_mode = WarnEnum(warn_mode.strip().upper())

    if warn_mode == WarnEnum.ALWAYS:
        if level == LogLevelEnum.EXCEPTION:
            _exc_info = sys.exc_info()
            await run_in_threadpool(logger.opt(exception=_exc_info).error, message)
        else:
            await run_in_threadpool(logger.log, level.name, message)

    elif warn_mode == WarnEnum.DEBUG:
        await run_in_threadpool(logger.debug, message)

    return


__all__ = [
    "async_log_at",
]
