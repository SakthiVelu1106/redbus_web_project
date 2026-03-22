"""
Logger utility for the RedBus Automation Framework.
Provides colored console logging with standardized format.
"""
import logging
import colorlog

# Color map for log levels
_LOG_COLORS = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

_loggers: dict[str, logging.Logger] = {}


def get_logger(name: str) -> logging.Logger:
    """
    Factory function that returns a named, colored logger.
    Reuses existing loggers to avoid duplicate handlers.

    Args:
        name: Logger name (typically __name__ of the calling module).

    Returns:
        Configured Logger instance.
    """
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Only add handler if none exist
    if not logger.handlers:
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                fmt="%(log_color)s%(asctime)s [%(levelname)-8s] %(name)s: %(message)s%(reset)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                log_colors=_LOG_COLORS,
            )
        )
        logger.addHandler(handler)

    # Prevent propagation to root logger to avoid duplicate output
    logger.propagate = False

    _loggers[name] = logger
    return logger
