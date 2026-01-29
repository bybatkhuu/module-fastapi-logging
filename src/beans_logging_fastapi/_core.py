from typing import TYPE_CHECKING

from pydantic import validate_call
from fastapi import FastAPI

if TYPE_CHECKING:
    from loguru import Record
    from loguru import Logger
else:
    from loguru._logger import Logger
    from loguru import logger  # noqa: F401

from beans_logging import Logger, LoggerLoader  # noqa: F811

from ._formats import http_file_format
from ._handlers import add_http_file_handler, add_http_file_json_handler
from ._middlewares import (
    HttpAccessLogMiddleware,
    RequestHTTPInfoMiddleware,
    ResponseHTTPInfoMiddleware,
)


@validate_call(config={"arbitrary_types_allowed": True})
def init_logger(app: FastAPI) -> "Logger":

    logger_loader = LoggerLoader()
    logger: Logger = logger_loader.load()  # noqa: F811

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

    app.add_middleware(ResponseHTTPInfoMiddleware)
    app.add_middleware(
        HttpAccessLogMiddleware,
        debug_format=logger_loader.config.extra.http_std_debug_format,  # type: ignore
        msg_format=logger_loader.config.extra.http_std_msg_format,  # type: ignore
    )
    app.add_middleware(
        RequestHTTPInfoMiddleware, has_proxy_headers=True, has_cf_headers=True
    )

    return logger


__all__ = [
    "init_logger",
]
