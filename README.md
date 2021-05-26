# awe-decorators
some very useful decorators for python (一些非常实用的 Python 装饰器)

## 安装

awedec 是 awesome decorators 前三个字母的简称

```sh
pip install awedec
```

## 装饰器介绍：

#### timeit

耗时统计装饰器，单位是秒，保留 4 位小数


使用方法：

```python
from awedec import timeit
@timeit()
def test_timeit():
    time.sleep(1)

#test_timeit cost 1.0026 seconds

@timeit(logger = your_logger)
def test_timeit():
    time.sleep(1)
```


#### retry

```python
from awedec import retry 

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


