from beans_logging.config import LoggerConfigPM


class FastAPIConfigPM(LoggerConfigPM):
    pass


class FastAPILoggerConfigPM(LoggerConfigPM):
    fastapi: dict = {}
