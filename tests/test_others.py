import os
import time
import unittest
from unittest.mock import MagicMock, patch
import dotenv
from somedecorators import (
    TimeoutError,
    email_on_exception,
    retry,
    timeit,
    timeout,
    wechat_on_exception,
)

dotenv.load_dotenv()


class MyException(Exception):
    pass


class DecoratorsTests(unittest.TestCase):
    def test_timeit(self):
        @timeit()
        def myfunc():
            time.sleep(0.01)
            return "done"

        output = myfunc()
        self.assertEqual(output, "done")

    def test_retry(self):
        @retry(times=1, wait_seconds=0, reraised_exception=MyException)
        def myfunc():
            raise Exception

        @retry(times=2, wait_seconds=0)
        def myfunc2():
            raise MyException

        self.assertRaises(MyException, myfunc)
        self.assertRaises(MyException, myfunc2)

    def test_timeout(self):
        @timeout(1)
        def do_something(args):
            time.sleep(args)

        with self.assertRaises(TimeoutError):
            do_something(2)

    @patch("somedecorators.wechat.WechatEnterprise")
    def test_wechat_on_exception(self, mock_wechat_cls):
        mock_we = MagicMock()
        mock_wechat_cls.return_value = mock_we

        @wechat_on_exception(["receiver1"], extra_msg="Severe Error")
        def myfunc(arg):
            return 1 / arg

        with self.assertRaises(ZeroDivisionError):
            myfunc(arg=0)

        mock_we.send_text.assert_called_once()

    @patch("somedecorators.email.send_mail")
    def test_email_on_exception(self, mock_send_mail):
        @email_on_exception(["test@example.com"], extra_msg="Severe Error")
        def myfunc(arg):
            return 1 / arg

        with self.assertRaises(ZeroDivisionError):
            myfunc(arg=0)

        mock_send_mail.assert_called_once()


if __name__ == "__main__":
    unittest.main()
