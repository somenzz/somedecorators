from awedec.timeit import timeit
from awedec.retry import retry
import logging

logger = logging.getLogger()
import time


class myException(Exception):
    pass


class CustomException(Exception):
    pass


@timeit()
def test_timeit():
    time.sleep(1)


@timeit()
@retry(
    times=2,
    wait_seconds=1,
    traced_exceptions=myException,
    reraised_exception=CustomException,
)
def test_retry():
    # time.sleep(1)
    raise myException


test_timeit()
test_retry()
