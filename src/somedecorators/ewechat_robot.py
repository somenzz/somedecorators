from functools import wraps
import json
import http.client
from urllib.parse import urlparse

def send_wechat_robot_message(url, content, mentioned_list=None):
    """
    Send a message to a WeChat webhook using Python's standard library.

    Parameters:
    - url (str): The webhook URL.
    - content (str): The message content to send.

    Returns:
    - bool: True if the message was sent successfully, False otherwise.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "msgtype": "text",
        "text": {"content": content, "mentioned_list": mentioned_list},
    }
    payload = json.dumps(payload)
    parsed_url = urlparse(url)
    connection = http.client.HTTPSConnection(parsed_url.netloc)
    path_with_query = f"{parsed_url.path}?{parsed_url.query}"
    try:
        connection.request("POST",path_with_query, body=payload, headers=headers)        
        response = connection.getresponse()        
        if response.status == 200:
            return True
    except Exception as e:
        # Handle connection errors, timeouts, etc.
        return False
    finally:
        connection.close()

    return False




def robot_on_exception(
    webhook_url, mentioned_list = None, traced_exceptions=None, extra_msg=None
):
    """
    当被装饰的函数调用抛出指定的异常时，发送机器人消息到群里，可以@指定人员
    webhook_url: 机器人 webhook url.
    mentioned_list: 必选，一个字符串列表，每项都是一个企业微信通讯录@人员账号。
    traced_exceptions: 可选，为监控的异常，可以为 None（默认）、异常类、或者一个异常类的元组。
                       如果为 None，则监控所有的异常；
                       如果指定了异常类，则函数调用抛出指定的异常时，发送消息。
    extra_msg: 可选，额外的信息。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            send = False
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if traced_exceptions is None:  # 说明要捕捉所有异常
                    send = True
                elif type(traced_exceptions) == list:
                    if type(e) in traced_exceptions:  # 如果指定了捕捉异常类的列表
                        send = True
                elif isinstance(e, traced_exceptions):  # 如果指定了捕捉的异常类
                    send = True
                else:
                    send = False
                if send:
                    send_wechat_robot_message(
                        url=webhook_url,
                        content=f"{extra_msg}: {func.__name__} raise Exception: {e}",
                        mentioned_list=mentioned_list,
                    )
                raise

        return wrapper

    return decorator
