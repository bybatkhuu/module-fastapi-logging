from pydantic import validate_call
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/")
def root():
    return {"Hello": "World"}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@router.get("/continue", status_code=100)
def get_continue():
    return {}


@router.get("/redirect")
def redirect():
    return RedirectResponse("/")


@router.get("/error")
def error():
    raise HTTPException(status_code=500)


@validate_call(config={"arbitrary_types_allowed": True})
def add_routers(app: FastAPI) -> None:
    """Add routers to FastAPI app.

    Args:
        app (FastAPI): FastAPI app instance.
    """

    app.include_router(router)

    return


__all__ = ["add_routers"]
