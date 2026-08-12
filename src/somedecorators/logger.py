import importlib
import logging
import logging.config
import os
import sys
from typing import Any, Callable, Optional, Union
import yaml


class ConfigurableNotificationHandler(logging.Handler):
    """
    Custom notification handler supporting callback as callable function or import path string.
    """

    def __init__(self, callback: Union[Callable, str], **kwargs: Any):
        super().__init__(**kwargs)

        if callable(callback):
            self.notify_callback = callback
        elif isinstance(callback, str):
            try:
                module_name, func_name = callback.rsplit(".", 1)
                module = importlib.import_module(module_name)
                self.notify_callback = getattr(module, func_name)
            except Exception as e:
                raise ImportError(f"Failed to load notification callback function '{callback}': {e}")
        else:
            raise ValueError("callback must be a callable object or a function path string")

    def emit(self, record: logging.LogRecord) -> None:
        if not hasattr(self, "notify_callback"):
            return
        try:
            msg = self.format(record)
            self.notify_callback(msg, record.levelname)
        except Exception:
            self.handleError(record)


def _setup_logging(
    log_level: str = "INFO",
    notify_callback: Optional[Union[Callable, str]] = None,
    notify_level: Union[str, int] = "WARNING",
    config_path: str = "logging.yaml",
) -> None:
    """Initialize global logging configuration (internal function)."""
    os.makedirs("logs", exist_ok=True)

    DEFAULT_LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "standard",
            },
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": log_level,
                "formatter": "detailed",
                "filename": "logs/app.log",
                "when": "D",
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "": {  # Root Logger
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": True,
            },
            "urllib3": {
                "handlers": [],
                "level": "ERROR",
                "propagate": True,
            },
        },
    }

    config_loaded_from_yaml = False

    if not os.path.exists(config_path):
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                yaml.dump(DEFAULT_LOGGING_CONFIG, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        except Exception:
            pass

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                logging.config.dictConfig(config)
                config_loaded_from_yaml = True
        except Exception:
            pass

    if not config_loaded_from_yaml:
        logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)

    root_logger = logging.getLogger()
    # Remove existing notification handlers to avoid duplication on re-init
    root_logger.handlers = [h for h in root_logger.handlers if not isinstance(h, ConfigurableNotificationHandler)]

    if notify_callback:
        notify_handler = ConfigurableNotificationHandler(callback=notify_callback)
        if isinstance(notify_level, str):
            notify_level = notify_level.upper()
        notify_handler.setLevel(notify_level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
        )
        notify_handler.setFormatter(formatter)
        root_logger.addHandler(notify_handler)


def _setup_exception_hook() -> None:
    """Configure global uncaught exception hook (internal function)."""
    root_logger = logging.getLogger()

    def handle_uncaught_exception(exc_type: type, exc_value: BaseException, exc_traceback: Any) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        root_logger.critical(
            "An uncaught global exception occurred:",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    sys.excepthook = handle_uncaught_exception


def init_app_logging(
    log_level: str = "INFO",
    notify_callback: Optional[Union[Callable, str]] = None,
    notify_level: Union[str, int] = "WARNING",
    config_path: str = "logging.yaml",
) -> None:
    """
    Unified logging initialization interface.

    :param log_level: Console and file output logging level (e.g. "DEBUG", "INFO", "WARNING").
    :param notify_callback: Optional callback callable or string import path (e.g., 'pkg.module.send_alert').
    :param notify_level: Notification trigger level (defaults to "WARNING").
    :param config_path: Path to logging YAML configuration file (defaults to "logging.yaml").
    """
    _setup_logging(log_level=log_level, notify_callback=notify_callback, notify_level=notify_level, config_path=config_path)
    _setup_exception_hook()

    status = "Enabled" if notify_callback else "Disabled"
    logging.getLogger(__name__).info(
        f"Logging system initialized (Level: {log_level}, Notification module: {status}, Notify level: {notify_level})"
    )
