from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Record

from beans_logging.filters import all_handlers_filter


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


__all__ = [
    "http_filter",
]
