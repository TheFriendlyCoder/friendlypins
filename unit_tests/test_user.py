import pytest
import mock
from friendlypins.user import User

def test_get_boards():
    data = dict()
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
