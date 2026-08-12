from functools import wraps
import http.client
import json
import logging
from typing import Any, Callable, List, Optional, Sequence, Tuple, Type, Union
from urllib.parse import urlparse
from .utils import should_catch_exception

logger = logging.getLogger(__name__)


def send_wechat_robot_message(url: str, content: str, mentioned_list: Optional[List[str]] = None) -> bool:
    """
    Send a text message to an Enterprise WeChat webhook robot.

    :param url: The WeChat robot webhook URL.
    :param content: Message body content.
    :param mentioned_list: Optional list of user IDs or '@all' to mention.
    :return: True if successfully sent (HTTP 200), False otherwise.
    """
    if not url:
        logger.error("WeChat robot webhook URL is empty.")
        return False

    headers = {"Content-Type": "application/json"}
    payload = {
        "msgtype": "text",
        "text": {"content": content, "mentioned_list": mentioned_list or []},
    }
    encoded_payload = json.dumps(payload)
    parsed_url = urlparse(url)

    connection = None
    try:
        connection = http.client.HTTPSConnection(parsed_url.netloc, timeout=10)
        path_with_query = f"{parsed_url.path}?{parsed_url.query}" if parsed_url.query else parsed_url.path
        connection.request("POST", path_with_query, body=encoded_payload, headers=headers)
        response = connection.getresponse()
        return response.status == 200
    except Exception as e:
        logger.error(f"Failed to send WeChat robot message: {e}")
        return False
    finally:
        if connection:
            connection.close()


def robot_on_exception(
    webhook_url: str,
    mentioned_list: Optional[List[str]] = None,
    traced_exceptions: Optional[Union[Type[BaseException], Sequence[Type[BaseException]], Tuple[Type[BaseException], ...]]] = None,
    extra_msg: Optional[str] = None,
) -> Callable:
    """
    Decorator that sends a webhook notification to Enterprise WeChat group when an exception occurs.

    :param webhook_url: Enterprise WeChat robot webhook URL.
    :param mentioned_list: Optional list of user IDs or '@all' to mention in group chat.
    :param traced_exceptions: Exception or collection of exceptions to monitor (default: None, catches all).
    :param extra_msg: Optional extra message string prefix for the alert message.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if should_catch_exception(e, traced_exceptions):
                    content = f"{extra_msg}: {func.__name__} raised {type(e).__name__}: {e}" if extra_msg else f"{func.__name__} raised {type(e).__name__}: {e}"
                    send_wechat_robot_message(
                        url=webhook_url,
                        content=content,
                        mentioned_list=mentioned_list,
                    )
                raise

        return wrapper

    return decorator
