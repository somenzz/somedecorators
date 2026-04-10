import sys
from somedecorators import init_app_logging
init_app_logging()
import logging
logger = logging.getLogger(__name__)


def test_logger2():
    logger.error("test error")

def test_logger():
    logger.info("test info")

