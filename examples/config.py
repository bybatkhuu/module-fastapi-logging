import os

from pydantic_settings import BaseSettings

from potato_util import io as io_utils
from beans_logging_fastapi import FastAPILoggerConfigPM


_config_path = os.path.join(os.getcwd(), "configs", "logger.yml")
_config_data = {}
if os.path.isfile(_config_path):
    _config_data = io_utils.read_config_file(config_path=_config_path)


class MainConfig(BaseSettings):
    logger: FastAPILoggerConfigPM = FastAPILoggerConfigPM()


config = MainConfig(**_config_data)


__all__ = [
    "MainConfig",
    "config",
]
