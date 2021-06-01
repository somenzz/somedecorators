from functools import wraps
from djangomail import send_mail
from djangomail.conf import settings
import traceback


def email_on_exception(recipient_list, traced_exceptions=None):
    """
    报错发邮件装饰器
    当被装饰的函数调用抛出指定的异常时，函数发送邮件给指定的人员
    recipient_list: 一个字符串列表，每项都是一个邮箱地址。recipient_list 中的每个成员都可以在邮件的 "收件人:" 中看到其他的收件人。
    traced_exceptions 为监控的异常，可以为 None（默认）、异常类、或者一个异常类的元组。
    traced_exceptions 如果为 None，则监控所有的异常；如果指定了异常类，则若函数调用抛出指定的异常时，发送邮件。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            recipients = recipient_list
            send = False
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if traced_exceptions is None:  # 说明要捕捉所有异常
                    send = True
                elif (
                    type(traced_exceptions) == list and type(e) in traced_exceptions
                ):  # 如果指定了捕捉异常类的列表，则 pass
                    send = True
                elif isinstance(e, traced_exceptions):  # 如果指定了捕捉的异常类
                    send = True
                else:
                    send = False
                if send:
                    send_mail(
                        subject=f"{func.__name__}'s Exception",
                        message= f"{func.__name__}'s Exception: {e} \n traceback:\n {traceback.format_exc()}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=recipients,
                    )
                
                raise

        return wrapper

    return decorator
