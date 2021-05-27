# awe-decorators
some very useful decorators for python (一些非常实用的 Python 装饰器)

## 安装

```sh
pip install somenzz-decorators
```

## 装饰器介绍：

#### timeit

耗时统计装饰器，单位是秒，保留 4 位小数


使用方法：

```python
from somenzz.decorators import timeit
@timeit()
def test_timeit():
    time.sleep(1)

#test_timeit cost 1.0026 seconds

@timeit(logger = your_logger)
def test_timeit():
    time.sleep(1)
```


#### retry

重试装饰器
- 当被装饰的函数调用抛出指定的异常时，函数会被重新调用。
- 直到达到指定的最大调用次数才重新抛出指定的异常，可以指定时间间隔，默认 5 秒后重试。
- traced_exceptions 为监控的异常，可以为 None（默认）、异常类、或者一个异常类的列表或元组 tuple。
- traced_exceptions 如果为 None，则监控所有的异常；如果指定了异常类，则若函数调用抛出指定的异常时，重新调用函数，直至成功返回结果。
- 未出现监控的异常时，如果指定定了 reraised_exception 则抛出 reraised_exception，否则抛出原来的异常。


```python
from somenzz.decorators import retry 

@retry(
    times=2,
    wait_seconds=1,
    traced_exceptions=myException,
    reraised_exception=CustomException,
)
def test_retry():
    # time.sleep(1)
    raise myException


test_retry()
```

## 参与项目

欢迎分享你最常用的装饰器，加入到这里。


