# Standard libraries
from typing import Any
from collections.abc import Callable

# Third-party libraries
import uvicorn
from uvicorn._types import ASGIApplication
from pydantic import validate_call
from fastapi import FastAPI

from beans_logging_fastapi import add_logger

# Internal modules
from __version__ import __version__
from config import config
from lifespan import lifespan
from router import add_routers


def create_app() -> FastAPI:
    """Create FastAPI application instance.

    Returns:
        FastAPI: FastAPI application instance.
    """

    app = FastAPI(lifespan=lifespan, version=__version__)

    # Add logger before any other components:
    add_logger(app=app, config=config.logger)

    # Add any other components after logger:
    add_routers(app=app)

    return app


@validate_call(config={"arbitrary_types_allowed": True})
def run_server(
    app: FastAPI | ASGIApplication | Callable[..., Any] | str = "main:app",
) -> None:
    """Run uvicorn server.

    Args:
        app (Union[ASGIApplication, str], optional): ASGI application instance or module path.
    """

    uvicorn.run(
        app=app,
        host="0.0.0.0",  # nosec B104
        port=8000,
        access_log=False,  # Disable default uvicorn access log
        server_header=False,
        proxy_headers=False,
        forwarded_allow_ips="*",
    )

    return


__all__ = [
    "create_app",
    "run_server",
]
