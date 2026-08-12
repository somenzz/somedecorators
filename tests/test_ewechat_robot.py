import os
import unittest
from unittest.mock import MagicMock, patch
import dotenv
from somedecorators.ewechat_robot import robot_on_exception, send_wechat_robot_message as send_wechat_robot_message_st

dotenv.load_dotenv()
url = os.getenv("ewechat_robot_url", "https://example.com/webhook")


class TestSendWechatRobotMessage(unittest.TestCase):
    @patch("somedecorators.ewechat_robot.http.client.HTTPSConnection")
    def test_send_wechat_robot_message_success(self, mock_https_connection):
        mock_response = MagicMock()
        mock_response.status = 200

        mock_connection = MagicMock()
        mock_connection.getresponse.return_value = mock_response
        mock_https_connection.return_value = mock_connection

        result = send_wechat_robot_message_st(url, "Hello, world!", ["user1"])
        self.assertTrue(result)

    @patch("somedecorators.ewechat_robot.http.client.HTTPSConnection")
    def test_send_wechat_robot_message_failure(self, mock_https_connection):
        mock_response = MagicMock()
        mock_response.status = 500

        mock_connection = MagicMock()
        mock_connection.getresponse.return_value = mock_response
        mock_https_connection.return_value = mock_connection

        result = send_wechat_robot_message_st(url, "Hello, world!", ["user1"])
        self.assertFalse(result)

    @patch("somedecorators.ewechat_robot.http.client.HTTPSConnection")
    def test_send_wechat_robot_message_exception(self, mock_https_connection):
        mock_connection = MagicMock()
        mock_connection.request.side_effect = Exception("Connection failed")
        mock_https_connection.return_value = mock_connection

        result = send_wechat_robot_message_st(url, "Hello, world!", ["user1"])
        self.assertFalse(result)

    @patch("somedecorators.ewechat_robot.send_wechat_robot_message")
    def test_robot_on_exception_decorator(self, mock_send):
        mock_send.return_value = True

        @robot_on_exception(webhook_url="https://example.com/webhook", extra_msg="Critical")
        def failing_func():
            raise ValueError("Test error")

        with self.assertRaises(ValueError):
            failing_func()

        mock_send.assert_called_once()
        self.assertIn("Critical: failing_func raised ValueError: Test error", mock_send.call_args[1]["content"])

    @unittest.skipUnless(os.getenv("RUN_REAL_WECHAT_TEST") == "1", "Real network test skipped by default")
    def test_send_wechat_robot_message_real(self):
        result = send_wechat_robot_message_st(url, "Hello, st world!")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
