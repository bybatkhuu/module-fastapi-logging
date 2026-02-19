from typing import Any

from pydantic import validate_call
from fastapi import Request
from fastapi.concurrency import run_in_threadpool

from beans_logging import logger, Logger


@validate_call(config={"arbitrary_types_allowed": True})
async def async_log_http_error(
    request: Request,
    status_code: int,
    msg_format_str: str = (
        '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u>'
        ' HTTP/{http_version}" <n>{status_code}</n>'
    ),
) -> None:
    """Async Log HTTP error for unhandled Exception.

    Args:
        request        (Request, required): Request instance.
        status_code    (int    , required): HTTP status code.
        msg_format_str (str    , optional): Message format. Defaults to
            '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}"
                <n>{status_code}</n>'.
    """

    _http_info: dict[str, Any] = {"request_id": request.state.request_id}
    if hasattr(request.state, "http_info") and isinstance(
        request.state.http_info, dict
    ):
        _http_info: dict[str, Any] = request.state.http_info
    _http_info["status_code"] = status_code

    _msg = msg_format_str.format(**_http_info)
    _logger: Logger = logger.opt(colors=True, record=True).bind(http_info=_http_info)
    await run_in_threadpool(_logger.error, _msg)
    return


@validate_call(config={"arbitrary_types_allowed": True})
def log_http_error(
    request: Request,
    status_code: int,
    msg_format_str: str = (
        '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u>'
        ' HTTP/{http_version}" <n>{status_code}</n>'
    ),
) -> None:
    """Log HTTP error for unhandled Exception.

    Args:
        request        (Request, required): Request instance.
        status_code    (int    , required): HTTP status code.
        msg_format_str (str    , optional): Message format. Defaults to
            '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}"
                <n>{status_code}</n>'.
    """

    _http_info: dict[str, Any] = {"request_id": request.state.request_id}
    if hasattr(request.state, "http_info") and isinstance(
        request.state.http_info, dict
    ):
        _http_info: dict[str, Any] = request.state.http_info
    _http_info["status_code"] = status_code

    _msg = msg_format_str.format(**_http_info)
    _logger: Logger = logger.opt(colors=True, record=True).bind(http_info=_http_info)
    _logger.error(_msg)
    return


__all__ = [
    "async_log_http_error",
    "log_http_error",
]
