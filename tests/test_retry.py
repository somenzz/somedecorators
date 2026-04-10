import unittest
from unittest.mock import MagicMock
from somedecorators import retry, MaxRetriesReachedException  # 请确保替换为你的文件名

class TestRetryDecorator(unittest.TestCase):

    def test_retry_on_false_enabled(self):
        """测试：当 is_false_retry=True 时，返回 False 应该触发重试"""
        # 创建一个模拟函数，每次调用都返回 False
        mock_func = MagicMock(return_value=False)
        
        # 应用装饰器，设置等待时间为 0 以加快测试速度
        @retry(times=3, wait_seconds=0, is_false_retry=True)
        def decorated_func():
            return mock_func()

        result = decorated_func()
        
        # 验证：函数应该被调用了 3 次（初始 1 次 + 重试 2 次）
        self.assertEqual(mock_func.call_count, 3)
        self.assertFalse(result)

    def test_retry_on_false_disabled(self):
        """测试：当 is_false_retry=False 时，返回 False 不应重试"""
        mock_func = MagicMock(return_value=False)
        
        @retry(times=3, wait_seconds=0, is_false_retry=False)
        def decorated_func():
            return mock_func()

        result = decorated_func()
        
        # 验证：函数只被调用了 1 次
        self.assertEqual(mock_func.call_count, 1)
        self.assertFalse(result)

    def test_retry_on_exception(self):
        """测试：传统的异常重试逻辑是否依然有效"""
        mock_func = MagicMock(side_effect=ValueError("Test Error"))
        
        @retry(times=2, wait_seconds=0, traced_exceptions=ValueError)
        def decorated_func():
            return mock_func()

        # 验证：达到最大次数后应该抛出异常
        with self.assertRaises(ValueError):
            decorated_func()
        
        self.assertEqual(mock_func.call_count, 2)

    def test_return_true_no_retry(self):
        """测试：正常返回非 False 值时不应重试"""
        mock_func = MagicMock(return_value="Success")
        
        @retry(times=5, wait_seconds=0, is_false_retry=True)
        def decorated_func():
            return mock_func()

        result = decorated_func()
        
        self.assertEqual(result, "Success")
        self.assertEqual(mock_func.call_count, 1)

if __name__ == '__main__':
    unittest.main()
