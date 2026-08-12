from functools import wraps
import signal
import time
from typing import Any, Callable, Optional


class TimeoutError(Exception):
    """An operation timed out."""
    pass


def timeit(_func: Optional[Any] = None, *, logger: Optional[Any] = None) -> Callable:
    """
    Timer decorator measuring execution time in seconds (4 decimal precision).
    Can be used as @timeit, @timeit(), or @timeit(logger=my_logger).

    :param _func: Internal positional parameter when used as @timeit without parentheses.
    :param logger: Optional logger instance or callable for outputting the timing message.
    """
    actual_logger = logger

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            cost = end - start
            msg = f"{func.__name__} cost {cost:.4f} seconds"

            if actual_logger:
                if hasattr(actual_logger, "info"):
                    actual_logger.info(msg)
                elif callable(actual_logger):
                    actual_logger(msg)
            else:
                print(msg)

            return result

        return wrapper

    if _func is None:
        return decorator

    if callable(_func):
        if hasattr(_func, "info"):
            actual_logger = _func
            return decorator
        return decorator(_func)

    actual_logger = _func
    return decorator


def timeout(seconds: int) -> Callable:
    """
    Raises a TimeoutError if a function does not terminate within specified seconds.
    Note: Requires OS signal support (SIGALRM, Unix/Linux/macOS main thread).

    :param seconds: Timeout limit in seconds.
    """
    if not hasattr(signal, "SIGALRM"):
        raise NotImplementedError("timeout decorator requires signal.SIGALRM, which is not supported on this platform.")

    def _timeout_error(signum: int, frame: Any) -> None:
        raise TimeoutError(f"Operation did not finish within {seconds} seconds")

    def timeout_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def timeout_wrapper(*args: Any, **kwargs: Any) -> Any:
            old_handler = signal.signal(signal.SIGALRM, _timeout_error)
            signal.alarm(seconds)
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)

        return timeout_wrapper

    return timeout_decorator
