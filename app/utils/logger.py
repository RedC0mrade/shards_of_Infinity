import logging
import sys
from config import settings

LOG_COLORS = {
    "DEBUG": "\033[36m",   # Cyan
    "INFO": "\033[32m",    # Green
    "WARNING": "\033[33m", # Yellow
    "ERROR": "\033[31m",   # Red
    "CRITICAL": "\033[41m",# Red background
    "RESET": "\033[0m",
}


class ColorFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        color = LOG_COLORS.get(levelname, "")
        reset = LOG_COLORS["RESET"]
        record.levelname = f"{color}{levelname}{reset}"
        record.msg = f"{record.msg}"
        return super().format(record)


def _resolve_log_level(level) -> int:
    """
    Преобразует уровень логирования из строки ('info') или числа
    в корректное числовое значение logging.
    """
    if isinstance(level, int):
        return level
    if isinstance(level, str):
        mapping = logging.getLevelNamesMapping()
        upper = level.upper()
        if upper in mapping:
            return mapping[upper]
        raise ValueError(f"Unknown log level string: {level}")
    raise ValueError(f"Unsupported log level type: {type(level)}")


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        level = _resolve_log_level(settings.logging.log_level)
        logger.setLevel(level)

        formatter = ColorFormatter(
            settings.logging.log_format, datefmt="%Y-%m-%d %H:%M:%S"
        )

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.propagate = False

    return logger
