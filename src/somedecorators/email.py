from functools import wraps
from typing import Any, Callable, List, Optional, Sequence, Tuple, Type, Union
from djangomail import send_mail
from .conf import settings
from .utils import args_to_str, format_exception_message, should_catch_exception


def email_on_exception(
    recipient_list: List[str],
    traced_exceptions: Optional[Union[Type[BaseException], Sequence[Type[BaseException]], Tuple[Type[BaseException], ...]]] = None,
    extra_msg: Optional[str] = None,
) -> Callable:
    """
    Decorator that sends an email notification via djangomail when the decorated function raises a matching exception.

    :param recipient_list: List of recipient email addresses.
    :param traced_exceptions: Exception or collection of exceptions to monitor (default: None, catches all).
    :param extra_msg: Optional extra message string appended to the email body.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if should_catch_exception(e, traced_exceptions):
                    message = format_exception_message(func, args, kwargs, e, extra_msg=extra_msg)
                    subject_args = args_to_str(*args, **kwargs)
                    subject = f"{func.__name__}({subject_args}) raise Exception" if subject_args else f"{func.__name__}() raise Exception"
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=recipient_list,
                    )
                raise

        return wrapper

    return decorator
