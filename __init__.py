# flake8: noqa

try:
    from .src.beans_logging_fastapi import *
except ImportError:
    from src.beans_logging_fastapi import *  # type: ignore
