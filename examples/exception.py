from collections.abc import Callable

from pydantic import validate_call
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from beans_logging_fastapi import log_http_error

from config import config


async def server_error_middleware(
    request: Request,
    call_next: Callable,
) -> Response:
    try:
        return await call_next(request)
    except Exception as exc:
        log_http_error(
            request=request,
            status_code=500,
            exc=exc,
            sub_format=config.logger.http.std.err_sub_format,
        )

        return JSONResponse(status_code=500, content={"message": "Server error"})


def server_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Server error handler.

    Args:
        request (Request  , required): Request instance.
        exc     (Exception, required): Exception instance.
    """

    log_http_error(
        request=request,
        status_code=500,
        exc=exc,
        sub_format=config.logger.http.std.err_sub_format,
    )

    return JSONResponse(status_code=500, content={"message": "Server error"})


@validate_call(config={"arbitrary_types_allowed": True})
def add_exception_handlers(app: FastAPI) -> None:
    """Add exception handlers to FastAPI application.

    Args:
        app (FastAPI): FastAPI application instance.
    """

    app.middleware("http")(server_error_middleware)
    app.add_exception_handler(500, server_error_handler)
    # Add more exception handlers here...

    return


__all__ = ["add_exception_handlers"]
