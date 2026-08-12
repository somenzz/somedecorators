from functools import wraps
from typing import Any, Callable, List, Optional, Sequence, Tuple, Type, Union
from wechat_enterprise import WechatEnterprise
from .conf import settings
from .utils import format_exception_message, should_catch_exception


def wechat_on_exception(
    recipient_list: List[str],
    traced_exceptions: Optional[Union[Type[BaseException], Sequence[Type[BaseException]], Tuple[Type[BaseException], ...]]] = None,
    extra_msg: Optional[str] = None,
) -> Callable:
    """
    Decorator that sends an enterprise WeChat message when the decorated function raises a matching exception.

    :param recipient_list: List of WeChat user IDs in enterprise WeChat directory.
    :param traced_exceptions: Exception or collection of exceptions to monitor (default: None, catches all).
    :param extra_msg: Optional extra message string appended to the alert message.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if should_catch_exception(e, traced_exceptions):
                    message = format_exception_message(func, args, kwargs, e, extra_msg=extra_msg)
                    we = WechatEnterprise(
                        corpid=settings.CORPID,
                        appid=settings.APPID,
                        corpsecret=settings.CORPSECRET,
                    )
                    we.send_text(message, recipient_list)
                raise

        return wrapper

    return decorator
