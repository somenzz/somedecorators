from somedecorators.log import setup_logger
from logging import getLogger


def test_logger2():
    logger2 = getLogger("myapp")
    logger1 = setup_logger("myapp")
    assert logger1 is logger2


def test_logger():
    logger1 = setup_logger("myapp")
    logger2 = getLogger("myapp")
    assert logger1 is logger2

