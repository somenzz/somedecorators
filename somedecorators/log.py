import os
import logging
from logging.handlers import TimedRotatingFileHandler
import sys


def setup_logger(name, level=logging.INFO):
    if not os.path.exists("logs"):
        os.mkdir("logs")
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)  # Set the logging level
    ch = logging.StreamHandler()
    # Create a handler that writes log messages to a file, with a new file created each day
    fh = TimedRotatingFileHandler(
        "logs/logfile.log", when="midnight", interval=1, backupCount=7
    )
    fh.suffix = "%Y-%m-%d.log"  # You can use strftime-based format for the suffix

    formatter = logging.Formatter(
        "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
    )
    formatter2 = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    fh.setFormatter(formatter)
    ch.setFormatter(formatter2)

    logger.addHandler(ch)  # 将日志输出至屏幕
    logger.addHandler(fh)  # 将日志输出至文件

    def handle_exception(exc_type, exc_value, exc_traceback):
        """Log any uncaught exceptions."""
        if issubclass(exc_type, KeyboardInterrupt):
            # Do not log or print KeyboardInterrupt exceptions (like Ctrl+C)
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.error(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    # Set the global exception hook to our custom function
    sys.excepthook = handle_exception

    return logger
