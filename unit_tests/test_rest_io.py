import pytest
import mock
from friendlypins.utils.rest_io import RestIO

@mock.patch("friendlypins.utils.rest_io.requests")
def test_get_method(mock_requests):
    expected_token = "1234abcd"
    obj = RestIO(expected_token)

    expected_path = "me/boards"
    expected_result = {
        "id": "abcd1234"
    }
    mock_response = mock.MagicMock()
    mock_response.json.return_value = expected_result
    mock_requests.get.return_value = mock_response
    res = obj.get(expected_path)

    assert res == expected_result
    mock_requests.get.assert_called_once()
    mock_response.raise_for_status.assert_called_once()
    assert expected_path in mock_requests.get.call_args[0][0]
    assert "access_token" in mock_requests.get.call_args[1]['params']
    assert mock_requests.get.call_args[1]['params']['access_token'] == expected_token

@mock.patch("friendlypins.utils.rest_io.requests")
def test_get_headers(mock_requests):
    obj = RestIO("1234abcd")
    assert obj.headers is None

    expected_bytes = 1024
    mock_response = mock.MagicMock()
    mock_response.headers = {
        "Content-Length": str(expected_bytes)
    }
    mock_requests.get.return_value = mock_response
    obj.get("me/boards")

    mock_requests.get.assert_called_once()

    tmp = obj.headers
    assert tmp is not None
    assert tmp.bytes == expected_bytes


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
