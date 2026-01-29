# Third-party libraries
import uvicorn
from uvicorn._types import ASGIApplication
from pydantic import validate_call
from fastapi import FastAPI

from beans_logging_fastapi import init_logger

# Internal modules
from __version__ import __version__
from lifespan import lifespan
from middleware import add_middlewares
from router import add_routers
from mount import add_mounts
from exception import add_exception_handlers


def create_app() -> FastAPI:
    """Create FastAPI application instance.

    Returns:
        FastAPI: FastAPI application instance.
    """

    app = FastAPI(version=__version__, lifespan=lifespan)

    init_logger(app=app)

    add_middlewares(app=app)
    add_routers(app=app)
    add_mounts(app=app)
    add_exception_handlers(app=app)

    return app


@validate_call(config={"arbitrary_types_allowed": True})
def run_server(app: ASGIApplication | str = "main:app") -> None:
    """Run uvicorn server.

    Args:
        app (Union[ASGIApplication, str], optional): ASGI application instance or module path.
    """

    uvicorn.run(
        app="main:app",
        host="0.0.0.0",  # nosec B104
        port=8000,
        access_log=False,
        server_header=False,
        proxy_headers=False,
        forwarded_allow_ips="*",
    )

    return


__all__ = [
    "create_app",
    "run_server",
]
