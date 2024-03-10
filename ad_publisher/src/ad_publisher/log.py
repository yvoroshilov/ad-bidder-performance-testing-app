import logging
from enum import Enum

from ad_publisher.config import LOG_LEVEL

LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


class LogLevel(str, Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    DEBUG = "DEBUG"

    def __str__(self):
        return str.__str__(self)


def configure_logging():
    log_level = str(LOG_LEVEL).upper()
    log_levels = list(LogLevel)

    if log_level not in log_levels:
        default_log_level = LogLevel.ERROR
        logging.warning(f"Unknown logger level provided: {log_level}. Defaulting to {default_log_level}")
        logging.basicConfig(level=str(default_log_level))
        return

    if log_level == LogLevel.DEBUG:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
    else:
        logging.basicConfig(level=log_level)
    logging.getLogger("httpcore").setLevel("INFO")
    logging.getLogger("httpx").setLevel("INFO")
