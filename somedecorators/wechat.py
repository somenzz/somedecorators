from functools import wraps
import traceback
from .conf import settings
from wechat_enterprise import WechatEnterprise

#接收者 ID，在企业微信通讯录中查看
#receivers = settings.RECEIVERS
# 发送 文本
#we.send_text("来息 somenzz 的消息", receivers)
# 发送 Markdown
#we.send_markdown("# Markdown", receivers)
# 发送图片
#we.send_image("/Users/aaron/Downloads/images.jpeg", receivers)
# 发送文件
#we.send_file("./wechat_enterprise.py", receivers)


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

def wechat_on_exception(recipient_list, traced_exceptions=None,extra_msg = None):
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
                    message= f"{func.__name__}({args_to_str(*args, **kwargs)}) raise Exception: {e} \n traceback:\n {traceback.format_exc()}\nextra_msg = {extra_msg}"
                    we = WechatEnterprise(
                        corpid=settings.CORPID,  # 企业 ID
                        appid=settings.APPID,  # 企业应用 ID
                        corpsecret=settings.CORPSECRET,  # 企业应用 Secret
                    )
                    #print(f"we.send_text({message},{recipients})")
                    we.send_text(message, recipients)
                raise

        return wrapper

    return decorator
