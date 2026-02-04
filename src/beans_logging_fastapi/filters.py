from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Record

from beans_logging.filters import all_handlers_filter

from .constants import HTTP_ACCESS_STD_HANDLER_NAME


def http_filter(record: "Record") -> bool:
    """Filter message only for http access log handler by checking 'http_info' key in extra.

    Args:
        record (Record, required): Log record as dictionary.

    Returns:
        bool: True if record has 'http_info' key in extra, False otherwise.
    """

    if not all_handlers_filter(record):
        return False

    if "http_info" not in record["extra"]:
        return False

    return True


def http_std_filter(record: "Record") -> bool:
    """Filter message only for http std log handler.

    Args:
        record (Record, required): Log record as dictionary.

    Returns:
        bool: True if record does not have 'disable_{HTTP_ACCESS_STD_HANDLER_NAME}' key in extra, False otherwise.
    """

    if not http_filter(record):
        return False

    if record["extra"].get(f"disable_{HTTP_ACCESS_STD_HANDLER_NAME}", False):
        return False

    return True


def http_all_file_filter(record: "Record") -> bool:
    """Filter message only for http file log handler.

    Args:
        record (Record, required): Log record as dictionary.

    Returns:
        bool: True if record does not have 'disable_http_all_file_handlers' key in extra, False otherwise.
    """

    if not http_filter(record):
        return False

    if record["extra"].get("disable_http_all_file_handlers", False):
        return False

    return True


__all__ = [
    "http_filter",
    "http_std_filter",
    "http_all_file_filter",
]
