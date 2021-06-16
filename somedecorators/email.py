from functools import wraps
from djangomail import send_mail
from djangomail.conf import settings
import traceback

def args_to_str(*args,**kwargs):
    str1 = ", ".join(str(i) for i in args)
    kv = []
    for k,v in kwargs.items():
        kv.append(f"{k}={v}")
    str2 = ", ".join(kv)
    if kwargs and args:
        return f"{str1}, {str2}"
    if args:
        return str1
    if kwargs:
        return str2
    return ''

def email_on_exception(recipient_list, traced_exceptions=None,extra_msg = None):
    """
    当被装饰的函数调用抛出指定的异常时，发送邮件给指定的人员
    recipient_list: 必选，一个字符串列表，每项都是一个邮箱地址。
    traced_exceptions: 可选，为监控的异常，可以为 None（默认）、异常类、或者一个异常类的元组。
                       如果为 None，则监控所有的异常； 
                       如果指定了异常类，则函数调用抛出指定的异常时，发送邮件。
    extra_msg: 可选，额外的信息。
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
                elif type(traced_exceptions) == list:
                    if type(e) in traced_exceptions:# 如果指定了捕捉异常类的列表
                        send = True
                elif isinstance(e, traced_exceptions):  # 如果指定了捕捉的异常类
                    send = True
                else:
                    send = False
                if send:
                    send_mail(
                        subject=f"{func.__name__}({args_to_str(*args, **kwargs)}) raise Exception",
                        message= f"{func.__name__}({args_to_str(*args, **kwargs)}) raise Exception: {e} \n "
                                 f"traceback:\n {traceback.format_exc()}\nextra_msg = {extra_msg}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=recipients,
                    )
                raise

        return wrapper

    return decorator
