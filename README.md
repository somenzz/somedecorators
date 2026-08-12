# somedecorators

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**somedecorators** is a production-ready suite of practical Python decorators, utility classes, and functions for logging, retries, performance measurement, timeout enforcement, configuration management, and multi-channel error notification (Email, Enterprise WeChat App, Enterprise WeChat Robot Webhook).

---

## 🌟 Features Overview

| Feature | Type | Description |
| :--- | :--- | :--- |
| `@retry` | Decorator | Automatic function retries on exceptions or `False` return values with configurable wait intervals and custom exceptions. |
| `@timeit` | Decorator | High-precision execution timing decorator. Supports `@timeit`, `@timeit()`, or `@timeit(logger=...)`. |
| `@timeout` | Decorator | Function timeout enforcement raising `TimeoutError` when runtime exceeds limits. |
| `@email_on_exception` | Decorator | Sends email notifications on uncaught exceptions using `djangomail`. |
| `@wechat_on_exception` | Decorator | Sends Enterprise WeChat notifications on uncaught exceptions. |
| `@robot_on_exception` | Decorator | Posts alert messages to Enterprise WeChat robot webhooks, with optional `@user` mentions. |
| `send_wechat_robot_message` | Function | Send custom text messages to Enterprise WeChat robot webhooks. |
| `init_app_logging` | Function | One-line global logging configuration with auto `logging.yaml` generation and notification hook. |
| `ConfigManager` | Class | Thread-safe singleton configuration loader supporting JSON & YAML format with defensive copying. |

---

## 📦 Installation

Install via `pip`:

```bash
pip install somedecorators
```

For development and testing:

```bash
pip install somedecorators[dev]
```

---

## 🚀 Quick Start & Usage

### 1. Function Retry (`@retry`)

Automatic retry handler supporting both exception-triggered and value-triggered (retrying when returning `False`) retries.

#### Key Parameters:
- `times` (*int*, default `3`): Maximum retry attempts.
- `wait_seconds` (*int/float*, default `5`): Delay between retries.
- `traced_exceptions` (*Exception | tuple | list | None*, default `None`): Exceptions to monitor (monitors all exceptions if `None`).
- `reraised_exception` (*Exception | None*, default `None`): Custom exception class or instance to raise when max retries are exhausted.
- `is_false_retry` (*bool*, default `False`): If `True`, retry when function returns `False`.

#### Code Example:

```python
from somedecorators import retry

# Basic usage: Retry up to 3 times with 2-second delay
@retry(times=3, wait_seconds=2)
def fetch_api_data():
    print("Requesting API...")
    raise ConnectionError("Network timeout")

# Retry when return value is False
@retry(times=5, wait_seconds=1, is_false_retry=True)
def check_status():
    return False

# Custom exception filtering & custom error on exhaustion
class ServiceUnavailable(Exception):
    pass

@retry(times=3, wait_seconds=1, traced_exceptions=(ValueError, KeyError), reraised_exception=ServiceUnavailable("Service failed after retries"))
def process_task():
    raise ValueError("Invalid payload")
```

---

### 2. High-Precision Timing (`@timeit`)

Monotonic timer decorator measuring execution duration in seconds (4 decimal precision).

#### Flexible Usage:

```python
import logging
import time
from somedecorators import timeit

# Usage 1: Bare decorator (outputs to print)
@timeit
def compute_data():
    time.sleep(0.5)

# Usage 2: Called without parameters
@timeit()
def run_job():
    time.sleep(0.2)

# Usage 3: Log output using custom logger instance
logger = logging.getLogger(__name__)

@timeit(logger=logger)
def process_records():
    time.sleep(0.1)

# Usage 4: Log output using a custom callable function
@timeit(logger=print)
def task():
    time.sleep(0.05)
```

---

### 3. Execution Timeout (`@timeout`)

Raises `TimeoutError` if the decorated function execution time exceeds the specified duration.

> **Note**: Requires Unix `signal.SIGALRM` support (Linux, macOS main thread).

```python
import time
from somedecorators import timeout, TimeoutError

@timeout(seconds=2)
def long_running_task():
    time.sleep(5)

try:
    long_running_task()
except TimeoutError as e:
    print(f"Task timed out: {e}")
```

---

### 4. Enterprise WeChat Robot Alerts (`@robot_on_exception` & `send_wechat_robot_message`)

Sends alerts to an Enterprise WeChat group webhook robot when a function raises an exception.

```python
from somedecorators import robot_on_exception, send_wechat_robot_message

WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"

# Decorator usage (with @mentions and extra message)
@robot_on_exception(
    webhook_url=WEBHOOK_URL,
    mentioned_list=["@all", "User1"],
    extra_msg="Production Service Failure"
)
def execute_pipeline():
    raise RuntimeError("Database connection lost")

# Direct function usage
success = send_wechat_robot_message(
    url=WEBHOOK_URL,
    content="Deployment completed successfully.",
    mentioned_list=["@all"]
)
```

---

### 5. Email Exception Alerts (`@email_on_exception`)

Sends exception tracebacks to recipient email addresses via `djangomail`.

#### Prerequisites:
Configure `settings.py` (or set `SETTINGS_MODULE` environment variable):

```python
# settings.py
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'your_email@163.com'
EMAIL_HOST_PASSWORD = 'your_authorization_code'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

#### Usage:

```python
from somedecorators import email_on_exception

@email_on_exception(
    recipient_list=['alert_admin@example.com'],
    traced_exceptions=(ZeroDivisionError, ValueError),
    extra_msg="Critical error in calculation worker"
)
def calculate(a, b):
    return a / b

calculate(1, 0)
```

---

### 6. Enterprise WeChat App Alerts (`@wechat_on_exception`)

Sends exception notifications to specific Enterprise WeChat users.

#### Prerequisites:
Add Enterprise WeChat credentials to `settings.py`:

```python
CORPID = "your_corp_id"
APPID = "your_app_id"
CORPSECRET = "your_corp_secret"
```

#### Usage:

```python
from somedecorators import wechat_on_exception

@wechat_on_exception(recipient_list=['UserAccount1', 'UserAccount2'], extra_msg="Payment Service Error")
def process_payment():
    raise Exception("Payment gateway unreachable")
```

---

### 7. Unified Application Logging (`init_app_logging`)

Zero-config global logging setup with automatic YAML generation, fallback safety, uncaught exception hook, and optional alert callbacks.

```python
import logging
from somedecorators import init_app_logging

# Option A: Simple initialization (auto-generates logging.yaml)
init_app_logging(log_level="INFO")

# Option B: Attach real-time notification callback
def on_alert(msg, levelname):
    print(f"[ALERT - {levelname}] {msg}")

init_app_logging(log_level="INFO", notify_callback=on_alert, notify_level="WARNING")

logger = logging.getLogger(__name__)
logger.info("Application initialized.")
logger.error("Something went wrong!")  # Triggers on_alert callback
```

---

### 8. Configuration Management (`ConfigManager`)

Thread-safe singleton configuration reader for JSON and YAML files with defensive copying.

```python
from somedecorators import ConfigManager

# Load configuration (supports .json, .yml, .yaml)
config = ConfigManager("config.yml")

# Access values
db_host = config.get("database.host", default="localhost")
all_settings = config.get_all()

# Reset singleton instance (useful during testing)
ConfigManager.reset()
```

---

## 🧪 Running Tests

Run the complete test suite using `pytest`:

```bash
./venv/bin/pytest -v
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
