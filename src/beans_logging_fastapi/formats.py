import json
from typing import Any
from zoneinfo import ZoneInfo
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Record


def http_file_format(
    record: "Record",
    format_: str = (
        '{client_host} {request_id} {user_id} [{datetime}] "{method} {url_path} HTTP/{http_version}" '
        '{status_code} {content_length} "{h_referer}" "{h_user_agent}" {response_time}'
    ),
    tz: str = "localtime",
) -> str:
    """Http access log file format.

    Args:
        record  (Record, required): Log record as dictionary.
        format_ (str   , optional): Log message format.
        tz      (str   , optional): Timezone for datetime field. Defaults to 'localtime'.

    Returns:
        str: Format for http access log record.
    """

    if "http_info" not in record["extra"]:
        return ""

    if "http_message" in record["extra"]:
        del record["extra"]["http_message"]

    _http_info: dict[str, Any] = record["extra"]["http_info"]
    if "datetime" not in _http_info:
        _dt = record["time"]
        if tz != "localtime":
            if not _dt.tzinfo:
                _dt = _dt.replace(tzinfo=ZoneInfo("UTC"))

            _dt = _dt.astimezone(ZoneInfo(tz))

        _http_info["datetime"] = _dt.isoformat(timespec="milliseconds")

    if "content_length" not in _http_info:
        _http_info["content_length"] = 0

    if "h_referer" not in _http_info:
        _http_info["h_referer"] = "-"

    if "h_user_agent" not in _http_info:
        _http_info["h_user_agent"] = "-"

    if "response_time" not in _http_info:
        _http_info["response_time"] = 0

    record["extra"]["http_info"] = _http_info
    _msg = format_.format(**_http_info)

    record["extra"]["http_message"] = _msg
    return "{extra[http_message]}\n"


def http_json_format(record: "Record") -> str:
    """Http access json log file format.

    Args:
        record (Record, required): Log record as dictionary.

    Returns:
        str: Format for http access json log record.
    """

    if "http_info" not in record["extra"]:
        return ""

    if "datetime" not in record["extra"]["http_info"]:
        record["extra"]["http_info"]["datetime"] = record["time"].isoformat(
            timespec="milliseconds"
        )

    if "http_serialized" in record["extra"]:
        del record["extra"]["http_serialized"]

    _http_info = record["extra"]["http_info"]
    record["extra"]["http_serialized"] = json.dumps(_http_info)

    return "{extra[http_serialized]}\n"


def id_std_format(record: "Record") -> str:
    """Std output log format with user_id, trace_id, and request_id.

    Args:
        record (Record): Log record as dictionary.

    Returns:
        str: Format for std output log with user_id, trace_id, and request_id.
    """

    _user_id = record["extra"].get("user_id")
    _trace_id = record["extra"].get("trace_id")
    _request_id = record["extra"].get("request_id")
    _request_id_part = f" | <d><w>{_request_id}</w></d>" if _request_id else ""
    _trace_id_part = f" | <lc>{_trace_id}</lc>" if _trace_id else ""
    _user_id_part = f" | <m>{_user_id}</m>" if _user_id else ""

    _format = (
        "[<c>{time:YYYY-MM-DD HH:mm:ss.SSS Z}</c> | <level>{extra[level_short]:<5}</level> | <w>{name}:{line}</w>"
        f"{_request_id_part}{_trace_id_part}{_user_id_part}"
        "]: <level>{message}</level>\n"
    )
    return _format


def id_file_format(record: "Record") -> str:
    """File log format with user_id, trace_id, and request_id.

    Args:
        record (Record): Log record as dictionary.

    Returns:
        str: Format for file log with user_id, trace_id, and request_id.
    """

    _user_id = record["extra"].get("user_id")
    _trace_id = record["extra"].get("trace_id")
    _request_id = record["extra"].get("request_id")
    _request_id_part = f" | {_request_id}" if _request_id else ""
    _trace_id_part = f" | {_trace_id}" if _trace_id else ""
    _user_id_part = f" | {_user_id}" if _user_id else ""

    _format = (
        "[{time:YYYY-MM-DD HH:mm:ss.SSS Z} | {extra[level_short]:<5} | {name}:{line}"
        f"{_request_id_part}{_trace_id_part}{_user_id_part}"
        "]: {message}\n"
    )
    return _format


__all__ = [
    "http_file_format",
    "http_json_format",
    "id_std_format",
    "id_file_format",
]
