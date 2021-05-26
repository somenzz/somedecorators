


from functools import wraps
import time

def timeit(logger = None):
    '''
    耗时统计装饰器，单位是秒，保留 4 位小数
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            if logger:
                logger.info(f"{func.__name__} cost {end - start :.4f} seconds")
            else:
                print(f"{func.__name__} cost {end - start :.4f} seconds")
            return result
        return wrapper
    return decorator

