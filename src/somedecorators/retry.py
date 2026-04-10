from functools import wraps
import time


class MaxRetriesReachedException(Exception):
    pass


def retry(times=3, wait_seconds=5, traced_exceptions=None, reraised_exception=None, is_false_retry=False):
    """
    重试装饰器
    :param times: 最大重试次数
    :param wait_seconds: 重试间隔秒数
    :param traced_exceptions: 监控的异常类或元组
    :param reraised_exception: 最终抛出的自定义异常
    :param is_false_retry: bool型，如果为 True，函数返回 False 时也会重试
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            count = times

            while count > 0:
                need_raise = False
                try:
                    result = func(*args, **kwargs)

                    # --- 新增逻辑：检查返回值是否为 False 且需要重试 ---
                    if is_false_retry and result is False:
                        count -= 1
                        if count <= 0:
                            # 如果次数用完，根据配置抛出异常或返回当前结果
                            if reraised_exception:
                                raise reraised_exception
                            return result  # 或者根据需求抛出 MaxRetriesReachedException
                    else:
                        # 正常返回结果（不是 False，或者不需要针对 False 重试）
                        return result

                except Exception as e:
                    # 异常处理逻辑保持不变
                    if traced_exceptions is None:
                        count -= 1
                    elif isinstance(traced_exceptions, list): # 修正了原代码中 type(list) 的判断方式
                        if type(e) in traced_exceptions:
                            count -= 1
                        else:
                            need_raise = True
                    elif isinstance(e, traced_exceptions):
                        count -= 1
                    else:
                        need_raise = True

                    if need_raise or count <= 0:
                        if reraised_exception:
                            raise reraised_exception
                        raise e

                # 无论是异常重试还是 False 重试，统一等待
                time.sleep(wait_seconds)

        return wrapper

    return decorator


