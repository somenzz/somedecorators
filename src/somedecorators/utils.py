from functools import wraps
import traceback
from typing import Any, Callable, Optional, Sequence, Tuple, Type, Union

ExceptionType = Union[Type[BaseException], Tuple[Type[BaseException], ...], Sequence[Type[BaseException]]]


def args_to_str(*args: Any, **kwargs: Any) -> str:
    """
    Format *args and **kwargs into a human-readable parameter string.
    """
    str1 = ", ".join(str(i) for i in args)
    kv = [f"{k}={v}" for k, v in kwargs.items()]
    str2 = ", ".join(kv)
    if kwargs and args:
        return f"{str1}, {str2}"
    if args:
        return str1
    if kwargs:
        return str2
    return ""


def should_catch_exception(
    exc: Exception,
    traced_exceptions: Optional[Union[Type[BaseException], Sequence[Type[BaseException]], Tuple[Type[BaseException], ...]]] = None,
) -> bool:
    """
    Check whether an exception instance matches traced_exceptions specification.

    :param exc: The caught exception instance.
    :param traced_exceptions: Exception class, tuple/list of exception classes, or None (to catch all).
    :return: True if the exception should be handled/caught, False otherwise.
    """
    if traced_exceptions is None:
        return True

    if isinstance(traced_exceptions, (list, set, tuple)):
        # Convert to tuple for isinstance compatibility
        valid_exceptions = tuple(ex for ex in traced_exceptions if isinstance(ex, type) and issubclass(ex, BaseException))
        return isinstance(exc, valid_exceptions) if valid_exceptions else False

    if isinstance(traced_exceptions, type) and issubclass(traced_exceptions, BaseException):
        return isinstance(exc, traced_exceptions)

    return False


def format_exception_message(
    func: Callable[..., Any],
    args: Tuple[Any, ...],
    kwargs: dict,
    exc: Exception,
    extra_msg: Optional[str] = None,
    include_traceback: bool = True,
) -> str:
    """
    Build a standardized message string for exception notifications.
    """
    func_sig = f"{func.__name__}({args_to_str(*args, **kwargs)})"
    msg = f"{func_sig} raised {type(exc).__name__}: {exc}"

    if include_traceback:
        tb_str = traceback.format_exc()
        msg += f"\n\ntraceback:\n{tb_str}"

    if extra_msg:
        msg += f"\n\nextra_msg: {extra_msg}"

    return msg
