from typing import Any

import potato_util as utils
from pydantic import Field, field_validator

from beans_logging.constants import LogHandlerTypeEnum, DEFAULT_HANDLER_NAMES
from beans_logging.schemas import LogHandlerPM
from beans_logging.config import (
    get_default_handlers as get_base_handlers,
    ExtraBaseModel,
    InterceptConfigPM,
    LoggerConfigPM as BaseLoggerConfigPM,
)

from .constants import (
    HTTP_ACCESS_FILE_HANDLER_NAME,
    HTTP_ERR_FILE_HANDLER_NAME,
    HTTP_ACCESS_JSON_HANDLER_NAME,
    HTTP_ERR_JSON_HANDLER_NAME,
)


def get_default_handlers() -> dict[str, LogHandlerPM]:
    """Get fastapi default log handlers.

    Returns:
        dict[str, LogHandlerPM]: Default handlers as dictionary.
    """

    _base_handlers = get_base_handlers()
    for _name, _handler in _base_handlers.items():
        if _name in DEFAULT_HANDLER_NAMES:
            _handler.enabled = True

    _http_handlers: dict[str, LogHandlerPM] = {
        HTTP_ACCESS_FILE_HANDLER_NAME: LogHandlerPM(
            h_type=LogHandlerTypeEnum.FILE,
            sink="http/{app_name}.http-access.log",
        ),
        HTTP_ERR_FILE_HANDLER_NAME: LogHandlerPM(
            h_type=LogHandlerTypeEnum.FILE,
            sink="http/{app_name}.http-err.log",
            error=True,
        ),
        HTTP_ACCESS_JSON_HANDLER_NAME: LogHandlerPM(
            h_type=LogHandlerTypeEnum.FILE,
            sink="http.json/{app_name}.http-access.json.log",
        ),
        HTTP_ERR_JSON_HANDLER_NAME: LogHandlerPM(
            h_type=LogHandlerTypeEnum.FILE,
            sink="http.json/{app_name}.http-err.json.log",
            error=True,
        ),
    }

    _default_handlers = {**_base_handlers, **_http_handlers}
    return _default_handlers


def get_default_intercept() -> InterceptConfigPM:
    _default_intercept = InterceptConfigPM(mute_modules=["uvicorn.access"])
    return _default_intercept


class StdConfigPM(ExtraBaseModel):
    format_str: str = Field(
        default=(
            '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}"'
            " {status_code} {content_length}B {response_time}ms"
        ),
        min_length=8,
        max_length=512,
    )
    err_format_str: str = Field(
        default=(
            '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}"'
            " <n>{status_code}</n>"
        ),
        min_length=8,
        max_length=512,
    )
    debug_format_str: str = Field(
        default='<n>[{request_id}]</n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}"',
        min_length=8,
        max_length=512,
    )


class FileConfigPM(ExtraBaseModel):
    format_str: str = Field(
        default=(
            '{client_host} {request_id} {user_id} [{datetime}] "{method} {url_path} HTTP/{http_version}"'
            ' {status_code} {content_length} "{h_referer}" "{h_user_agent}" {response_time}'
        ),
        min_length=8,
        max_length=512,
    )
    tz: str = Field(default="localtime", min_length=2, max_length=64)


class HeadersConfigPM(ExtraBaseModel):
    has_proxy: bool = Field(default=False)
    has_cf: bool = Field(default=False)


class HttpConfigPM(ExtraBaseModel):
    std: StdConfigPM = Field(default_factory=StdConfigPM)
    file: FileConfigPM = Field(default_factory=FileConfigPM)
    headers: HeadersConfigPM = Field(default_factory=HeadersConfigPM)


class LoggerConfigPM(BaseLoggerConfigPM):
    http: HttpConfigPM = Field(default_factory=HttpConfigPM)
    intercept: InterceptConfigPM = Field(default_factory=get_default_intercept)
    handlers: dict[str, LogHandlerPM] = Field(default_factory=get_default_handlers)

    @field_validator("handlers", mode="before")
    @classmethod
    def _check_handlers(cls, val: Any) -> dict[str, LogHandlerPM]:

        _default_handlers = get_default_handlers()

        if not val:
            val = _default_handlers
            return val

        if not isinstance(val, dict):
            raise TypeError(
                f"'handlers' attribute type {type(val).__name__} is invalid, must be a dict of <LogHandlerPM> or dict!"
            )

        for _key, _handler in val.items():
            if not isinstance(_handler, (LogHandlerPM, dict)):
                raise TypeError(
                    f"'handlers' attribute's '{_key}' key -> value type {type(_handler).__name__} is invalid, must be "
                    f"<LogHandlerPM> or dict!"
                )

            if isinstance(_handler, LogHandlerPM):
                val[_key] = _handler.model_dump(
                    by_alias=True, exclude_unset=True, exclude_none=True
                )

        _default_dict = {
            _key: _handler.model_dump(
                by_alias=True, exclude_unset=True, exclude_none=True
            )
            for _key, _handler in _default_handlers.items()
        }

        if _default_dict != val:
            val = utils.deep_merge(_default_dict, val)

        for _key, _handler in val.items():
            val[_key] = LogHandlerPM(**_handler)

        return val


__all__ = [
    "LoggerConfigPM",
    "HttpConfigPM",
    "StdConfigPM",
    "FileConfigPM",
    "HeadersConfigPM",
    "get_default_intercept",
    "get_default_handlers",
]
