from typing import TYPE_CHECKING

from pydantic import validate_call
from fastapi import FastAPI

if TYPE_CHECKING:
    from loguru import Logger
else:
    from loguru._logger import Logger

from beans_logging import LoggerLoader

from .constants import (
    HTTP_ACCESS_FILE_HANDLER_NAME,
    HTTP_ERR_FILE_HANDLER_NAME,
    HTTP_ACCESS_JSON_HANDLER_NAME,
    HTTP_ERR_JSON_HANDLER_NAME,
)
from .config import FastAPILoggerConfigPM
from .filters import use_http_filter
from .formats import http_file_format, http_file_json_format
from .middlewares import (
    HttpAccessLogMiddleware,
    RequestHTTPInfoMiddleware,
    ResponseHTTPInfoMiddleware,
)


@validate_call(config={"arbitrary_types_allowed": True})
def add_logger(
    app: FastAPI,
    config: FastAPILoggerConfigPM,
    has_proxy_headers: bool | None = None,
    has_cf_headers: bool | None = None,
) -> "Logger":

    logger_loader = LoggerLoader(config=config)

    if has_proxy_headers is None:
        has_proxy_headers = config.http.headers.has_proxy

    if has_cf_headers is None:
        has_cf_headers = config.http.headers.has_cf

    app.add_middleware(ResponseHTTPInfoMiddleware)
    app.add_middleware(
        HttpAccessLogMiddleware,
        debug_format_str=config.http.std.debug_format_str,
        format_str=config.http.std.format_str,
    )
    app.add_middleware(
        RequestHTTPInfoMiddleware,
        has_proxy_headers=has_proxy_headers,
        has_cf_headers=has_cf_headers,
    )

    for _name, _handler in logger_loader.config.handlers.items():
        if (_name == HTTP_ACCESS_FILE_HANDLER_NAME) or (
            _name == HTTP_ERR_FILE_HANDLER_NAME
        ):
            _handler.filter_ = use_http_filter
            _handler.format_ = lambda record: http_file_format(
                record=record,
                format_str=config.http.file.format_str,
                tz=config.http.file.tz,
            )
        elif (_name == HTTP_ACCESS_JSON_HANDLER_NAME) or (
            _name == HTTP_ERR_JSON_HANDLER_NAME
        ):
            _handler.filter_ = use_http_filter
            _handler.format_ = http_file_json_format

    logger: Logger = logger_loader.load()
    return logger


__all__ = [
    "add_logger",
]
