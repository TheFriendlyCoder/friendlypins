import pytest
import mock
from friendlypins.api import API

def test_get_user():
    obj = API('abcd1234')
    expected_url = 'https://www.pinterest.com/MyUserName/'
    expected_firstname = "John"
    expected_lastname = "Doe"
    expected_id = 12345678
    expected_data = {
        'data': {
            'url': expected_url,
            'first_name': expected_firstname,
            'last_name': expected_lastname,
            'id': str(expected_id)
        }
    }
    with mock.patch("friendlypins.api.requests") as mock_requests:
        mock_response = mock.MagicMock()
        mock_response.json.return_value = expected_data
        mock_requests.get.return_value = mock_response
        result = obj.get_user()

        assert expected_url == result.url
        assert expected_firstname == result.first_name
        assert expected_lastname == result.last_name
        assert expected_id == result.unique_id


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
