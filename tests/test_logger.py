import logging
import pytest
from somedecorators import init_app_logging

logger = logging.getLogger(__name__)


def test_logger_basic():
    init_app_logging(log_level="INFO")
    logger.info("test info")
    logger.error("test error")


def test_notify_level_default():
    received = []

    def callback(msg, levelname):
        received.append((msg, levelname))

    init_app_logging(notify_callback=callback)  # default notify_level is "WARNING"
    test_log = logging.getLogger("test_notify_default")
    test_log.info("info msg")
    test_log.warning("warning msg")
    test_log.error("error msg")

    assert len(received) == 2
    assert received[0][1] == "WARNING"
    assert received[1][1] == "ERROR"


def test_notify_level_custom():
    received = []

    def callback(msg, levelname):
        received.append((msg, levelname))

    init_app_logging(notify_callback=callback, notify_level="ERROR")
    test_log = logging.getLogger("test_notify_custom")
    test_log.warning("warning msg")
    test_log.error("error msg")

    assert len(received) == 1
    assert received[0][1] == "ERROR"
