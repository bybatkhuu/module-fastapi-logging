import os

from pydantic_settings import BaseSettings

from potato_util import io as io_utils
from beans_logging_fastapi import LoggerConfigPM

from logger import logger

_config_dict = {}
_configs_dir = os.path.join(os.getcwd(), "configs")
if os.path.isdir(_configs_dir):
    _config_dict = io_utils.read_all_configs(configs_dir=_configs_dir)


class MainConfig(BaseSettings):
    logger: LoggerConfigPM = LoggerConfigPM()


try:
    config = MainConfig(**_config_dict)
except Exception:
    logger.exception("Failed to load config:")
    raise SystemExit(1)


__all__ = [
    "MainConfig",
    "config",
]
