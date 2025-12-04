#!/usr/bin/env python

from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

load_dotenv()

from beans_logging_fastapi import (  # noqa: E402
    HttpAccessLogMiddleware,
    RequestHTTPInfoMiddleware,
    ResponseHTTPInfoMiddleware,
)

from logger import logger, logger_loader  # noqa: E402
from __version__ import __version__  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Preparing to startup...")
    logger.success("Finished preparation to startup.")
    logger.info(f"API version: {__version__}")

    yield
    logger.info("Praparing to shutdown...")
    logger.success("Finished preparation to shutdown.")


app = FastAPI(lifespan=lifespan, version=__version__)

app.add_middleware(ResponseHTTPInfoMiddleware)
app.add_middleware(
    HttpAccessLogMiddleware,
    debug_format=logger_loader.config.extra.http_std_debug_format,  # type: ignore
    msg_format=logger_loader.config.extra.http_std_msg_format,  # type: ignore
)
app.add_middleware(
    RequestHTTPInfoMiddleware, has_proxy_headers=True, has_cf_headers=True
)


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.get("/continue", status_code=100)
def get_continue():
    return {}


@app.get("/redirect")
def redirect():
    return RedirectResponse("/")


@app.get("/error")
def error():
    raise HTTPException(status_code=500)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",  # nosec B104
        port=8000,
        access_log=False,
        server_header=False,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
