from pydantic import validate_call
from fastapi import FastAPI


@validate_call(config={"arbitrary_types_allowed": True})
def add_middlewares(app: FastAPI) -> None:
    """Add middlewares to FastAPI app.

    Args:
        app (FastAPI): FastAPI app instance.
    """

    # Add more middlewares here...

    return


__all__ = ["add_middlewares"]
