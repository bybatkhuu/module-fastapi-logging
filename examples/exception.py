from pydantic import validate_call
from fastapi import FastAPI


@validate_call(config={"arbitrary_types_allowed": True})
def add_exception_handlers(app: FastAPI) -> None:
    """Add exception handlers to FastAPI application.

    Args:
        app (FastAPI): FastAPI application instance.
    """
    # Add more exception handlers here...

    return


__all__ = ["add_exception_handlers"]
