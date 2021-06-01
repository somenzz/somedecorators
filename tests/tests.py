"""
Testing the decorators utility package.
"""

import unittest
import time
from somedecorators import timeit, retry, email_on_exception

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

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

    def test_email_on_exception(self):

        @email_on_exception(['somenzz@163.com'])
        def myfunc():
            1/0

        with self.assertRaises(ZeroDivisionError):
            myfunc()

        
if __name__ == '__main__':
    unittest.main()

