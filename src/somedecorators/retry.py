from functools import wraps
import time
from typing import Any, Callable, Optional, Sequence, Tuple, Type, Union
from .utils import should_catch_exception


class MaxRetriesReachedException(Exception):
    """Exception raised when maximum retry limit is reached."""
    pass


def retry(
    times: int = 3,
    wait_seconds: Union[int, float] = 5,
    traced_exceptions: Optional[Union[Type[BaseException], Sequence[Type[BaseException]], Tuple[Type[BaseException], ...]]] = None,
    reraised_exception: Optional[Union[Exception, Type[Exception]]] = None,
    is_false_retry: bool = False,
) -> Callable:
    """
    Retry decorator for functions that may fail or return False.

    :param times: Maximum retry attempts (default: 3).
    :param wait_seconds: Interval in seconds between retry attempts (default: 5).
    :param traced_exceptions: Exception or tuple/list of exceptions to catch and retry (default: None, catches all exceptions).
    :param reraised_exception: Custom exception to raise when retries are exhausted.
    :param is_false_retry: If True, retry when function returns False.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            count = times

            while count > 0:
                try:
                    result = func(*args, **kwargs)

                    if is_false_retry and result is False:
                        count -= 1
                        if count <= 0:
                            if reraised_exception:
                                raise reraised_exception if isinstance(reraised_exception, Exception) else reraised_exception()
                            return result
                    else:
                        return result

                except Exception as e:
                    if not should_catch_exception(e, traced_exceptions):
                        raise e

                    count -= 1
                    if count <= 0:
                        if reraised_exception:
                            raise reraised_exception if isinstance(reraised_exception, Exception) else reraised_exception()
                        raise e

                if wait_seconds > 0:
                    time.sleep(wait_seconds)

        return wrapper

    return decorator
