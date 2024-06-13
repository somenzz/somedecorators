import unittest
from unittest.mock import patch, MagicMock
from somedecorators.ewechat_robot import  send_wechat_robot_message as send_wechat_robot_message_st

url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c7a456a3-4c24-44a8-a140-13950c3585b9"


class TestSendWechatRobotMessage(unittest.TestCase):
    @patch('somedecorators.ewechat_robot.http.client.HTTPSConnection')
    def test_send_wechat_robot_message_success(self, mock_https_connection):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.getresponse.return_value = mock_response

        # Setup mock connection
        mock_connection = MagicMock()
        mock_connection.getresponse.return_value = mock_response
        mock_https_connection.return_value = mock_connection

        # Test function
        result = send_wechat_robot_message_st(url, 'Hello, world!', ['user1'])
        self.assertTrue(result)

    @patch('somedecorators.ewechat_robot.http.client.HTTPSConnection')
    def test_send_wechat_robot_message_failure(self, mock_https_connection):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500  # Simulate server error
        mock_response.getresponse.return_value = mock_response

        # Setup mock connection
        mock_connection = MagicMock()
        mock_connection.getresponse.return_value = mock_response
        mock_https_connection.return_value = mock_connection

        # Test function
        result = send_wechat_robot_message_st(url, 'Hello, world!', ['user1'])
        self.assertFalse(result)

    @patch('somedecorators.ewechat_robot.http.client.HTTPSConnection')
    def test_send_wechat_robot_message_exception(self, mock_https_connection):
        # Setup mock connection to raise an exception
        mock_connection = MagicMock()
        mock_connection.request.side_effect = Exception("Connection failed")
        mock_https_connection.return_value = mock_connection

        # Test function
        result = send_wechat_robot_message_st(url, 'Hello, world!', ['user1'])
        self.assertFalse(result)

    def test_send_wechat_robot_message_real(self):
        # Test function
        result = send_wechat_robot_message_st(url, 'Hello,st world!')        
        self.assertTrue(result)
        result = send_wechat_robot_message_st(url, 'Hello,st @ world!',mentioned_list=['DaZhengGe'])        
        self.assertTrue(result)
    

if __name__ == '__main__':
    unittest.main()
