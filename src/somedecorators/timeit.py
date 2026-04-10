from functools import wraps
import time
import signal


class TimeoutError(Exception):
    """
    An operation timed out
    """
    pass


def timeit(logger=None):
    """
    耗时统计装饰器，单位是秒，保留 4 位小数
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            if logger:
                logger.info(f"{func.__name__} cost {end - start :.4f} seconds")
            else:
                print(f"{func.__name__} cost {end - start :.4f} seconds")
            return result

        return wrapper

    return decorator



def timeout(seconds):
    """
    Raises a TimeoutError if a function does not terminate within
    specified seconds.
    """
    def _timeout_error(signal, frame):
        raise TimeoutError("Operation did not finish within {} seconds".format(seconds))

    def timeout_decorator(func):

        @wraps(func)
        def timeout_wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _timeout_error)
            signal.alarm(seconds)
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)

        return timeout_wrapper

    return timeout_decorator

