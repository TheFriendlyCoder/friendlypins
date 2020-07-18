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
def test_get_pages_one_page(mock_requests):
    expected_token = "1234abcd"
    obj = RestIO(expected_token)

    expected_path = "me/boards"
    expected_result = {
        "id": "abcd1234"
    }
    mock_response = mock.MagicMock()
    mock_response.json.return_value = expected_result
    mock_requests.get.return_value = mock_response
    res = list()
    for cur_res in obj.get_pages(expected_path):
        res.append(cur_res)

    assert len(res) == 1
    assert res[0] == expected_result
    mock_requests.get.assert_called_once()
    mock_response.raise_for_status.assert_called_once()
    assert expected_path in mock_requests.get.call_args[0][0]
    assert "access_token" in mock_requests.get.call_args[1]['params']
    assert mock_requests.get.call_args[1]['params']['access_token'] == expected_token


@mock.patch("friendlypins.utils.rest_io.requests")
def test_get_headers(mock_requests):
    obj = RestIO("1234abcd")

    expected_bytes = 1024
    mock_response = mock.MagicMock()
    mock_response.headers = {
        "Content-Length": str(expected_bytes)
    }
    mock_requests.get.return_value = mock_response
    obj.get("me/boards")
    tmp = obj.headers

    mock_requests.get.assert_called_once()
    assert tmp is not None
    assert tmp.bytes == expected_bytes


@mock.patch("friendlypins.utils.rest_io.requests")
def test_get_default_headers(mock_requests):
    obj = RestIO("1234abcd")

    expected_bytes = 1024
    mock_response = mock.MagicMock()
    mock_response.headers = {
        "Content-Length": str(expected_bytes)
    }
    mock_requests.get.return_value = mock_response

    tmp = obj.headers
    assert tmp is not None
    assert tmp.bytes == expected_bytes
    mock_requests.get.assert_called_once()


@mock.patch("friendlypins.utils.rest_io.requests")
def test_post(mock_requests):
    obj = RestIO("1234abcd")
    expected_path = "me/boards"
    expected_data = {
        "name": "My New Board",
        "description": "Here is my cool description"
    }

    expected_results = {
        "testing": "123"
    }
    mock_response = mock.MagicMock()
    mock_requests.post.return_value = mock_response
    mock_response.json.return_value = expected_results

    res = obj.post(expected_path, expected_data)

    mock_response.json.assert_called_once()
    mock_requests.post.assert_called_once()

    assert expected_path in mock_requests.post.call_args[0][0]
    assert "data" in mock_requests.post.call_args[1]
    assert mock_requests.post.call_args[1]["data"] == expected_data
    assert res == expected_results
