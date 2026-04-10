import logging
import logging.config
import importlib
import os
import sys
import yaml

class ConfigurableNotificationHandler(logging.Handler):
    """
    Custom notification handler.
    Supports passing an actual callable object or a function path string (e.g., 'notify.send_wechat_alert').
    """
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)

        if callable(callback):
            self.notify_callback = callback
        elif isinstance(callback, str):
            try:
                module_name, func_name = callback.rsplit('.', 1)
                module = importlib.import_module(module_name)
                self.notify_callback = getattr(module, func_name)
            except Exception as e:
                raise ImportError(f"Failed to load notification callback function '{callback}': {e}")
        else:
            raise ValueError("callback must be a callable object or a function path string")

    def emit(self, record):
        if not hasattr(self, 'notify_callback'):
            return
        try:
            # Format the log and call the externally loaded notification function
            msg = self.format(record)
            self.notify_callback(msg, record.levelname)
        except Exception:
            self.handleError(record)


def _setup_logging(log_level="INFO", notify_callback=None, config_path="logging.yaml"):
    """Initialize global logging configuration (internal function)"""
    os.makedirs("logs", exist_ok=True)

    # 1. Default basic configuration dictionary (Fallback)
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
            }
        },
        "loggers": {
            "": {  # Root Logger
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": True
            },
            "urllib3": { # Mute noise from third-party libraries
                "handlers": [],
                "level": "ERROR",
                "propagate": True
            }
        }
    }

    config_loaded_from_yaml = False

    # 2. If the configuration file does not exist, generate it using the default configuration
    if not os.path.exists(config_path):
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                # default_flow_style=False makes YAML generate an expanded readable format, sort_keys=False keeps original dictionary order
                yaml.dump(DEFAULT_LOGGING_CONFIG, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print(f"[*] {config_path} not found, automatically generated default logging configuration file.")
        except Exception as e:
            print(f"[!] Failed to automatically generate {config_path}: {e}. Will use memory configuration directly.")

    # 3. Attempt to read and apply YAML configuration
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                logging.config.dictConfig(config)
                config_loaded_from_yaml = True
        except Exception as e:
            print(f"[!] Failed to read or parse {config_path}: {e}. Falling back to system default configuration.")

    # 4. If YAML loading fails (whether it was not successfully generated or parsing error), use default memory configuration
    if not config_loaded_from_yaml:
        logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)

    # 5. If notify_callback is passed, dynamically mount the notification handler
    if notify_callback:
        notify_handler = ConfigurableNotificationHandler(callback=notify_callback)
        notify_handler.setLevel(logging.ERROR) # By default, only ERROR and above levels will trigger notifications

        # Set detailed format for the notification handler
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
        )
        notify_handler.setFormatter(formatter)

        # Get root logger and mount
        logging.getLogger().addHandler(notify_handler)


def _setup_exception_hook():
    """Configure global uncaught exception hook (internal function)"""
    root_logger = logging.getLogger()

    def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        root_logger.critical(
            "An uncaught global exception occurred:",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = handle_uncaught_exception


def init_app_logging(log_level="INFO", notify_callback=None, config_path="logging.yaml"):
    """
    Unified initialization interface exposed to the outside.
    Simply call this function once at project startup to complete all configuration.

    :param log_level: The logging output level for console and file, e.g., "DEBUG", "INFO", "WARNING".
    :param notify_callback: Optional. Pass a custom notification function object or import path string (e.g., 'utils.notify.send_alert'). If None, notifications are disabled.
    :param config_path: The path to the logging configuration file, defaults to "logging.yaml" in the current directory.
    """
    _setup_logging(log_level=log_level, notify_callback=notify_callback, config_path=config_path)
    _setup_exception_hook()

    status = 'Enabled' if notify_callback else 'Disabled'
    logging.getLogger(__name__).info(f"Logging system initialized (Level: {log_level}, Notification module: {status})")

