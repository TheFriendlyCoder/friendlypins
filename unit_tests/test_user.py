import pytest
import mock
from friendlypins.user import User

def test_user_properties():
    expected_url = 'https://www.pinterest.com/MyUserName/'
    expected_firstname = "John"
    expected_lastname = "Doe"
    expected_id = 12345678
    expected_board_count = 32
    expected_pin_count = 512
    data = {
        'url': expected_url,
        'first_name': expected_firstname,
        'last_name': expected_lastname,
        'id': str(expected_id),
        'counts': {
            'boards': str(expected_board_count),
            'pins': str(expected_pin_count)
        }
    }

    obj = User(data, "https://pinterest_url/v1", "1234abcd")
    assert expected_url == obj.url
    assert expected_firstname == obj.first_name
    assert expected_lastname == obj.last_name
    assert expected_id == obj.unique_id
    assert expected_board_count == obj.num_boards
    assert expected_pin_count == obj.num_pins


def test_get_boards():
    data = {
        "first_name": "John",
        "last_name": "Doe"
    }
    api_url = "https://pinterest_url/v1"
    token = "1234abcd"
    obj = User(data, api_url, token)

    expected_id = 1234
    expected_name = "MyBoard"
    expected_url = "https://www.pinterest.ca/MyName/MyBoard/"
    expected_data = {
        "data": [{
            "id": str(expected_id),
            "name": expected_name,
            "url": expected_url
        }]
    }

    with mock.patch("friendlypins.user.requests") as mock_requests:
        mock_response = mock.MagicMock()
        mock_response.json.return_value = expected_data
        mock_requests.get.return_value = mock_response
        result = obj.boards

        assert len(result) == 1
        assert expected_url == result[0].url
        assert expected_name == result[0].name
        assert expected_id == result[0].unique_id

        mock_response.raise_for_status.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
