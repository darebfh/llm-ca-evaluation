import unittest
from unittest.mock import patch
from src.evaluation.openai_client import send_data_to_api


class TestAPIClient(unittest.TestCase):
    @patch('src.evaluation.api_client.requests.post')
    def test_send_data_to_api(self, mock_post):
        # Test if data is sent to the API correctly
        api_url = 'http://example.com/api'
        test_data = ['John Doe', '25', 'New York']

        # Assume a successful response from the API
        mock_post.return_value.text = 'Success'

        send_data_to_api(api_url, [test_data])

        # Verify that the API is called with the correct data
        mock_post.assert_called_once_with(api_url, data=test_data)


if __name__ == '__main__':
    unittest.main()