"""
Testing the decorators utility package.
"""

import unittest
import time
from awedec import timeit, retry

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
            
        self.assertRaises(MyException, myfunc)


if __name__ == '__main__':
    unittest.main()

