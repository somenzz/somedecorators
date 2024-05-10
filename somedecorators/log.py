import logging.config
import os
import sys


def setup_logger(name=""):
    os.makedirs("logs", exist_ok=True)
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s [%(process)d] [%(thread)d] [%(levelname)s] [%(module)s:%(lineno)d] - %(message)s"
            },
            "simple": {
                "format": "%(asctime)s - %(levelname)s [%(module)s:%(lineno)d] - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "detailed",
                "filename": "logs/application.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": True,
            }
        },
    }

    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)


def handle_exception(exc_type, exc_value, exc_traceback):
    """Log any uncaught exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        # Do not log or print KeyboardInterrupt exceptions (like Ctrl+C)
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger = setup_logger()
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


# Set the global exception hook to our custom function
sys.excepthook = handle_exception
