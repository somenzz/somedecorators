# somedecorators

Some very useful Python decorators, functions, classes, continuously updated.


一些非常实用的 Python 装饰器、函数、类，持续更新。

- 新增 robot_on_exception，报错通过企业微信机器人发送至企业微信群聊 :  from somedecorators import robot_on_exception
- 新增 wechat_on_exception，报错发送企业微信 :  from somedecorators import wechat_on_exception
- 新增 init_app_logging 快速配置日志  : from somedecorators import init_app_logging
- 新增 ConfigManager，快速搞定配置文件 : from somedecorators import ConfigManager 

使用方法如下：

## 安装

```sh
pip install somedecorators
```

## 装饰器介绍：

#### 发送企业微信机器人

调用代码 
mentioned_list 参数可以不填写。
```python
@robot_on_exception(webhook_url= "你的企业威胁你机器人 webhook",mentioned_list=["@谁就填写谁的企业微信账号","user2"], extra_msg="运行报错")
def myfunc(args):
    if args == 1:
        raise Exception1
    elif args == 2:
        raise Exception2
    else:
        raise Exception3
```



#### timeit

耗时统计装饰器，单位是秒，保留 4 位小数


使用方法：

```python
from somedecorators import timeit
@timeit()
def test_timeit():
    time.sleep(1)

#test_timeit cost 1.0026 seconds

@timeit(logger = your_logger)
def test_timeit():
    time.sleep(1)
```


#### timeout

超时装饰器，单位是秒，函数运行超过指定的时间会抛出 TimeOutError 异常。

使用方法：

```python
import time
from somedecorators import timeout
@timeout(2)
def test_timeit():
    time.sleep(3)

#somedecorators.timeit.TimeoutError: Operation did not finish within 2 seconds
```



#### retry


这是一个功能强大且灵活的 Python 装饰器，用于自动处理函数失败后的重试逻辑。它不仅支持基于**特定异常**的重试，还支持根据**函数返回值**（如返回 `False`）触发重试。

###### 核心特性
* **自定义重试次数与间隔**：自由设定最大尝试次数及每次重试间的延迟。
* **精确的异常捕获**：可指定仅针对某些特定异常进行重试。
* **返回值监控**：支持当函数返回 `False` 时视作失败并触发重试。
* **异常重塑**：重试耗尽后，可以抛出原始异常或自定义的业务异常。

---

###### 参数说明

在函数上方使用 `@retry(...)` 即可调用。以下是可配置参数：

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `times` | `int` | `3` | 最大重试次数。 |
| `wait_seconds` | `int/float` | `5` | 每次重试之间的等待时间（秒）。 |
| `traced_exceptions` | `Exception` 或 `tuple` | `None` | 指定需要监控的异常。若为 `None`，则监控所有 `Exception`。 |
| `reraised_exception` | `Exception` | `None` | 当重试次数耗尽后，抛出的自定义异常类。 |
| `is_false_retry` | `bool` | `False` | 如果为 `True`，当函数返回结果为 `False` 时也会触发重试。 |

---

###### 快速上手示例

####### 1. 基础用法 (默认配置)
失败后最多重试 3 次，每次间隔 5 秒。
```python
@retry()
def unstable_api():
    print("尝试请求数据...")
    raise ConnectionError("网络不稳定")

# 结果：尝试 1 次 + 重试 3 次 = 总计 4 次调用后抛出 ConnectionError
```

####### 2. 指定异常重试

仅在捕获到 `ValueError` 时重试，遇到其他异常（如 `TypeError`）则立即崩溃。
```python
@retry(times=2, wait_seconds=1, traced_exceptions=ValueError)
def process_data(n):
    if n < 0:
        raise ValueError("输入不能为负数")
    return n
```

####### 3. 基于返回值的重试 (`is_false_retry`)

在某些业务场景下，函数不报错但返回 `False` 表示失败（例如检查登录状态）。

```python
@retry(times=5, wait_seconds=2, is_false_retry=True)
def check_service_status():
    # 假设该函数返回 True 或 False
    status = get_remote_status() 
    return status 
```

####### 4. 抛出自定义业务异常

当达到最大重试次数后，隐藏底层细节，抛出预定义的异常。
```python
class MyBusinessError(Exception):
    pass

@retry(times=3, reraised_exception=MyBusinessError("重试多次后依然失败，请检查配置"))
def upload_file():
    raise IOError("磁盘空间不足")
```



#### email_on_exception

报错发邮件装饰器。当被装饰的函数调用抛出指定的异常时，函数发送邮件给指定的人员，使用独立的 [djangomail](https://github.com/somenzz/djangomail) 发邮件模块，非常好用。

- recipient_list: 一个字符串列表，每项都是一个邮箱地址。recipient_list 中的每个成员都可以在邮件的 "收件人:" 中看到其他的收件人。
- traced_exceptions 为监控的异常，可以为 None（默认）、异常类、或者一个异常类的元组。
traced_exceptions 如果为 None，则监控所有的异常；如果指定了异常类，则若函数调用抛出指定的异常时，发送邮件。

**使用方法**：

首先在项目目录新建 settings.py，配置邮件服务器或企业微信，内容如下：

```python
EMAIL_USE_LOCALTIME = True

#for unitest
#EMAIL_BACKEND = 'djangomail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'djangomail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com' #可以换其他邮箱
EMAIL_PORT = 465
EMAIL_HOST_USER = 'your-username'
EMAIL_HOST_PASSWORD = '********'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER


# 用于发送企业微信
CORPID="**********************"  # 企业 ID
APPID="*******"  # 企业应用 ID
CORPSECRET="************************" # 企业应用 Secret

```

如果你的文件名不是 settings.py，假如是 mysettings.py 则需要修改环境变量:

```python
os.environ.setdefault("SETTINGS_MODULE", "mysettings")
```
然后主程序中这样使用：

##### 监控所有的异常

```python
from somedecorators import email_on_exception 
#import os
#os.environ.setdefault("SETTINGS_MODULE", "settings") #默认配置，可以不写此行代码

@email_on_exception(['somenzz@163.com'])
def myfunc(arg):
    1/arg

myfunc(0)
```

你会收到如下的邮件信息，非常便于排查错误。

```sh
Subject: myfunc(arg=0) raise Exception
From: your-username
To: somenzz@163.com
Date: Fri, 11 Jun 2021 20:55:01 -0500
Message-ID: 
 <162346290112.13869.15957310483971819045@1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa>

myfunc(arg=0) raise Exception: division by zero 
 traceback:
 Traceback (most recent call last):
  File "/Users/aaron/github/somenzz/somedecorators/somedecorators/email.py", line 35, in wrapper
    return func(*args, **kwargs)
  File "/Users/aaron/github/somenzz/somedecorators/tests/tests.py", line 55, in myfunc
    return 1/arg
ZeroDivisionError: division by zero

extra_msg = 严重错误
```

##### 监控指定的异常

```python

from somedecorators import email_on_exception
import os
os.environ.setdefault("SETTINGS_MODULE", "settings")

class Exception1(Exception):
    pass

class Exception2(Exception):
    pass

class Exception3(Exception):
    pass

@email_on_exception(['somenzz@163.com'],traced_exceptions = Exception2)
def myfunc(args):
    if args == 1:
        raise Exception1
    elif args == 2:
        raise Exception2
    else:
        raise Exception3

myfunc(2)

```
上述代码只有在 raise Exception2 时才会发送邮件：

##### 不同的异常发给不同的人

```python
@email_on_exception(['somenzz@163.com'],traced_exceptions = Exception2)
@email_on_exception(['others@163.com'],traced_exceptions = (Exception1, Exception3))
def myfunc(args):
    if args == 1:
        raise Exception1
    elif args == 2:
        raise Exception2
    else:
        raise Exception3
```

是不是非常方便？

#### 发送企业微信

发送前需要在 settings.py 文件企业微信相关信息

settings.py 示例：

```python

CORPID="**********************"  # 企业 ID
APPID="*******"  # 企业应用 ID
CORPSECRET="************************" # 企业应用 Secret

```

调用代码 

```python
@wechat_on_exception(['企业微信接收者ID'],traced_exceptions = Exception2)
def myfunc(args):
    if args == 1:
        raise Exception1
    elif args == 2:
        raise Exception2
    else:
        raise Exception3
```


#### 快速配置日志 init_app_logging

一个开箱即用、高可用且支持动态通知的 Python 日志模块。

###### ✨ 核心特性

* **开箱即用 (Auto-Bootstrap)**：首次运行自动生成 `logging.yaml` 配置文件，零配置成本。
* **优雅降级 (Graceful Fallback)**：当配置文件丢失或格式错误时，自动回退到内存安全配置，保证核心业务不中断。
* **全局异常捕获 (Exception Hook)**：自动接管 `sys.excepthook`，将未捕获的代码异常转为 `CRITICAL` 级别日志。
* **动态通知系统 (Dynamic Notifier)**：支持通过函数对象或字符串路径（依赖注入）动态挂载告警模块（如飞书、钉钉、微信、邮件告警），仅在 `ERROR` 及以上级别触发。

###### 📦 依赖与安装

本模块依赖 `PyYAML` 解析配置文件，请确保环境中已安装：

```bash
pip install PyYAML
```

###### 🚀 快速开始

在你的项目入口文件（如 `main.py` 或 `app.py`）的**最顶部**初始化一次即可，后续所有文件按 Python 原生方式使用 `logging` 即可。

####### 场景 1：基础使用（零配置）

如果不传入任何参数，系统将默认在当前目录寻找 `logging.yaml`。如果找不到，会自动生成一份并应用。

```python
import logging
from utils.log import init_app_logging

# 1. 在项目启动时初始化
init_app_logging(log_level="INFO")

# 2. 在任何文件中正常使用
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Application started successfully.")
    logger.error("This is an error message, but no notification is sent.")
    
    # 触发未捕获异常，将自动记录为 CRITICAL 并保存到文件
    # 1 / 0 
```

####### 场景 2：绑定实时告警通知（推荐）

你可以传入一个自定义的通知函数。当系统发生 `ERROR` 或 `CRITICAL` 级别（包括未捕获异常）时，会自动触发该函数。

```python
import logging
from utils.log import init_app_logging

# 定义你的通知函数 (需接收 msg 和 levelname 两个参数)
def my_webhook_alert(msg, levelname):
    # 这里可以实现请求企业微信/钉钉/飞书 API 的逻辑
    print(f"[ALERT triggered!] Level: {levelname} | Message: {msg}")

init_app_logging(log_level="INFO", notify_callback=my_webhook_alert)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Normal log, won't trigger alert.")
    logger.error("Database connection failed!") # 会触发 my_webhook_alert
```

####### 场景 3：配置文件驱动（字符串路径反射）

为了保持代码整洁，或者配合微服务架构，你可以直接传入通知函数的**字符串导入路径**，模块会利用反射机制动态加载。

```python
import logging
from utils.log import init_app_logging

# 假设你的发件函数在 services/alert_service.py 下的 send_wechat_msg 函数
init_app_logging(
    log_level="WARNING", 
    notify_callback="services.alert_service.send_wechat_msg"
)

logger = logging.getLogger(__name__)
logger.error("System crash!") # 动态加载并调用 send_wechat_msg
```

###### ⚙️ 配置文件说明 (`logging.yaml`)

项目首次启动后，如果根目录没有 `logging.yaml`，模块会自动生成该文件并默认创建 `logs/app.log` 目录进行日志按天切割归档（保留30天）。

生成的 `logging.yaml` 结构如下，你可以随时根据需要修改它：

```yaml
version: 1
disable_existing_loggers: false
formatters:
  standard:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: standard
  file:
    class: logging.handlers.TimedRotatingFileHandler
    level: INFO
    formatter: detailed
    filename: logs/app.log
    when: D
    interval: 1
    backupCount: 30
    encoding: utf-8
loggers:
  '':
    handlers:
    - console
    - file
    level: INFO
    propagate: true
  urllib3:
    handlers: []
    level: ERROR
    propagate: true
```
> **提示**：即使你删除了该文件，或者不小心写错了缩进导致解析失败，系统也能自动回退到默认的控制台+文件输出配置，确保业务不会因为日志组件的错误而崩溃。

###### 📚 API 参考

####### `init_app_logging(log_level="INFO", notify_callback=None, config_path="logging.yaml")`

* **`log_level`** *(str)*: 控制台和基础文件日志的级别。可选值：`"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`。
* **`notify_callback`** *(callable | str | None)*: 告警通知回调。支持直接传入函数对象，或类似 `'pkg.module.func'` 的字符串路径。设为 `None` 则不开启通知。
* **`config_path`** *(str)*: YAML 配置文件的路径，默认为当前工作目录下的 `"logging.yaml"`。

#### 快速搞定配置文件

```python
from somedecorators import ConfigManager
config_manager = ConfigManager("config.yml")
config_data = config_manager.get_all()
print(config_data)
```

## 参与项目

欢迎分享你最常用的装饰器、类、函数，加入到这里。

## 联系我 

微信：somenzz-enjoy
公众号：Python七号
