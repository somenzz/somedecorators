from functools import wraps
import time


class MaxRetriesReachedException(Exception):
    pass


def retry(times=3, wait_seconds=5, traced_exceptions=None, reraised_exception=None):
    """
    重试装饰器
    当被装饰的函数调用抛出指定的异常时，函数会被重新调用。
    直到达到指定的最大调用次数才重新抛出指定的异常，可以指定时间间隔，默认 5 秒后重试。
    traced_exceptions 为监控的异常，可以为 None（默认）、异常类、或者一个异常类的元组。
    traced_exceptions 如果为 None，则监控所有的异常；如果指定了异常类，则若函数调用抛出指定的异常时，重新调用函数，直至成功返回结果。
    未出现监控的异常时，如果指定定了 reraised_exception 则抛出 reraised_exception，否则抛出原来的异常。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            count = times
            need_raise = False
            while count > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if traced_exceptions is None:  # 说明要捕捉所有异常
                        count -= 1

                    elif type(traced_exceptions) == list:
                        if type(e) in traced_exceptions:# 如果指定了捕捉异常类的列表
                            count -= 1

                    elif isinstance(e, traced_exceptions):  # 如果指定了捕捉的异常类，或元组
                        count -= 1

                    else:  # 需要抛出异常 reraised_exception 为 None 则抛出原来的异常，否则只抛出指定的异常
                        need_raise = True

                    if need_raise or count <= 0:
                        if reraised_exception:
                            raise reraised_exception
                        raise
                    time.sleep(wait_seconds)

        return wrapper

    return decorator
