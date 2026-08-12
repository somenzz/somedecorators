import unittest
from unittest.mock import MagicMock
from somedecorators import MaxRetriesReachedException, retry


class TestRetryDecorator(unittest.TestCase):
    def test_retry_on_false_enabled(self):
        """Test: when is_false_retry=True, returning False triggers retry."""
        mock_func = MagicMock(return_value=False)

        @retry(times=3, wait_seconds=0, is_false_retry=True)
        def decorated_func():
            return mock_func()

        result = decorated_func()
        self.assertEqual(mock_func.call_count, 3)
        self.assertFalse(result)

    def test_retry_on_false_disabled(self):
        """Test: when is_false_retry=False, returning False does not retry."""
        mock_func = MagicMock(return_value=False)

        @retry(times=3, wait_seconds=0, is_false_retry=False)
        def decorated_func():
            return mock_func()

        result = decorated_func()
        self.assertEqual(mock_func.call_count, 1)
        self.assertFalse(result)

    def test_retry_on_exception(self):
        """Test: conventional exception retry logic."""
        mock_func = MagicMock(side_effect=ValueError("Test Error"))

        @retry(times=2, wait_seconds=0, traced_exceptions=ValueError)
        def decorated_func():
            return mock_func()

        with self.assertRaises(ValueError):
            decorated_func()

        self.assertEqual(mock_func.call_count, 2)

    def test_traced_exceptions_list_and_tuple(self):
        """Test: traced_exceptions supplied as list or tuple of exception types."""
        mock_func = MagicMock(side_effect=TypeError("Type Error"))

        @retry(times=2, wait_seconds=0, traced_exceptions=[ValueError, TypeError])
        def decorated_func():
            return mock_func()

        with self.assertRaises(TypeError):
            decorated_func()

        self.assertEqual(mock_func.call_count, 2)

    def test_untraced_exception_raises_immediately(self):
        """Test: exceptions not in traced_exceptions cause immediate failure."""
        mock_func = MagicMock(side_effect=KeyError("Key Error"))

        @retry(times=3, wait_seconds=0, traced_exceptions=ValueError)
        def decorated_func():
            return mock_func()

        with self.assertRaises(KeyError):
            decorated_func()

        self.assertEqual(mock_func.call_count, 1)

    def test_custom_reraised_exception(self):
        """Test: raising custom exception when retry attempts exhaust."""
        class CustomError(Exception):
            pass

        mock_func = MagicMock(side_effect=ValueError("Failed"))

        @retry(times=2, wait_seconds=0, reraised_exception=CustomError("Custom Exhausted"))
        def decorated_func():
            return mock_func()

        with self.assertRaises(CustomError):
            decorated_func()

    def test_return_true_no_retry(self):
        """Test: returning non-False value does not retry."""
        mock_func = MagicMock(return_value="Success")

        @retry(times=5, wait_seconds=0, is_false_retry=True)
        def decorated_func():
            return mock_func()

        result = decorated_func()
        self.assertEqual(result, "Success")
        self.assertEqual(mock_func.call_count, 1)


if __name__ == "__main__":
    unittest.main()
