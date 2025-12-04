from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Record

from beans_logging import Logger, LoggerLoader
from beans_logging_fastapi import (
    add_http_file_handler,
    add_http_file_json_handler,
    http_file_format,
)

logger_loader = LoggerLoader()
logger: Logger = logger_loader.load()


def _http_file_format(record: "Record") -> str:
    _format = http_file_format(
        record=record,
        msg_format=logger_loader.config.extra.http_file_format,  # type: ignore
        tz=logger_loader.config.extra.http_file_tz,  # type: ignore
    )
    return _format


if logger_loader.config.extra.http_file_enabled:  # type: ignore
    add_http_file_handler(
        logger_loader=logger_loader,
        log_path=logger_loader.config.extra.http_log_path,  # type: ignore
        err_path=logger_loader.config.extra.http_err_path,  # type: ignore
        formatter=_http_file_format,
    )

if logger_loader.config.extra.http_json_enabled:  # type: ignore
    add_http_file_json_handler(
        logger_loader=logger_loader,
        log_path=logger_loader.config.extra.http_json_path,  # type: ignore
        err_path=logger_loader.config.extra.http_json_err_path,  # type: ignore
    )


__all__ = [
    "logger",
    "logger_loader",
]
