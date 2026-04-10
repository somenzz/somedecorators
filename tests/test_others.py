"""
Testing the decorators utility package.
"""

import unittest
import time,os
from somedecorators import timeit, retry, email_on_exception,timeout
from somedecorators import TimeoutError
from somedecorators import wechat_on_exception
import dotenv
dotenv.load_dotenv()



class MyException(Exception):
    pass


class DecoratorsTests(unittest.TestCase):
    """
    Basic decorators utility tests.
    """

    def test_timeit(self):
        """
        Test the timeit decorator
        """

        @timeit()
        def myfunc():
            time.sleep(1)
            return "done"
        
        output = myfunc()
        self.assertEqual(len(output), 4)
        self.assertEqual(output, "done")

    def test_retry(self):
        """
        Test the timeit decorator
        """

        @retry(times = 1, wait_seconds = 1, reraised_exception = MyException)
        def myfunc():
            raise Exception

        @retry(times = 2, wait_seconds = 1)
        def myfunc2():
            raise MyException

        self.assertRaises(MyException, myfunc)
        self.assertRaises(MyException, myfunc2)

    def test_timeout(self):

        @timeout(2)
        def do_something(args):
            time.sleep(args)

        with self.assertRaises(TimeoutError):
            do_something(3)



    def test_wechat_on_exception(self):

        @wechat_on_exception([os.getenv("wechat_receiver")],extra_msg="严重错误")
        def myfunc(arg):
            print("begin test wechat on exception")
            return 1/arg
        with self.assertRaises(ZeroDivisionError):
            myfunc(arg = 0)


    def test_email_on_exception(self):

        @email_on_exception([os.getenv("email_recerver")],extra_msg="严重错误")
        def myfunc(arg):
            print("begin test email on exception")
            return 1/arg
        with self.assertRaises(ZeroDivisionError):
            myfunc(arg = 0)




if __name__ == '__main__':
    unittest.main()
