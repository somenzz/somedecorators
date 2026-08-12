import logging
import time
import unittest
from unittest.mock import MagicMock
from somedecorators.timeit import TimeoutError, timeit, timeout


class TestTimeitAndTimeout(unittest.TestCase):
    def test_timeit_without_parentheses(self):
        @timeit
        def my_func():
            time.sleep(0.01)
            return "done"

        result = my_func()
        self.assertEqual(result, "done")

    def test_timeit_with_empty_parentheses(self):
        @timeit()
        def my_func():
            time.sleep(0.01)
            return "done"

        result = my_func()
        self.assertEqual(result, "done")

    def test_timeit_with_logger(self):
        mock_logger = MagicMock()

        @timeit(logger=mock_logger)
        def my_func():
            time.sleep(0.01)
            return "result"

        res = my_func()
        self.assertEqual(res, "result")
        mock_logger.info.assert_called_once()
        self.assertIn("my_func cost", mock_logger.info.call_args[0][0])

    def test_timeit_with_callable_logger(self):
        logs = []

        def custom_logger(msg):
            logs.append(msg)

        @timeit(logger=custom_logger)
        def my_func():
            time.sleep(0.01)
            return 42

        res = my_func()
        self.assertEqual(res, 42)
        self.assertEqual(len(logs), 1)
        self.assertIn("my_func cost", logs[0])

    def test_timeout(self):
        @timeout(1)
        def fast_func():
            return "fast"

        self.assertEqual(fast_func(), "fast")

        @timeout(1)
        def slow_func():
            time.sleep(2)

        with self.assertRaises(TimeoutError):
            slow_func()


if __name__ == "__main__":
    unittest.main()
