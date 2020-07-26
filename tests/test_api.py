import mock
from friendlypins.api import API
from friendlypins.board import Board
from friendlypins.pin import Pin
from dateutil import tz


def test_get_user():
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
    with mock.patch("friendlypins.api.RestIO") as mock_io:
        mock_obj = mock.MagicMock()
        mock_obj.get.return_value = expected_data
        mock_io.return_value = mock_obj

        obj = API('abcd1234')
        result = obj.user

        assert expected_url == result.url
        assert expected_firstname == result.first_name
        assert expected_lastname == result.last_name
        assert expected_id == result.unique_id


@mock.patch("friendlypins.utils.rest_io.requests")
def test_get_board_by_id(mock_requests):
    mock_response = mock.MagicMock()
    mock_requests.get.return_value = mock_response

    obj = API("abcd1234")
    result = obj.get_board_by_id("1234")
    assert result is not None
    assert isinstance(result, Board)
    assert mock_requests.get.call_count == 0


@mock.patch("friendlypins.utils.rest_io.requests")
def test_get_pin_by_id(mock_requests):
    mock_response = mock.MagicMock()
    mock_requests.get.return_value = mock_response

    obj = API("abcd1234")
    result = obj.get_pin_by_id("1234")
    assert result is not None
    assert isinstance(result, Pin)
    assert mock_requests.get.call_count == 0


@mock.patch("friendlypins.utils.rest_io.requests")
def test_transaction_limit(mock_requests):
    mock_response = mock.MagicMock()
    expected_rate_limit = 100
    mock_response.headers = {
      'Access-Control-Allow-Origin': '*',
      'Age': '0',
      'Cache-Control': 'private',
      'Content-Encoding': 'gzip',
      'Content-Type': 'application/json',
      'Pinterest-Version': 'e3f92ef',
      'X-Content-Type-Options': 'nosniff',
      'X-Pinterest-RID': '12345678',
      'X-Ratelimit-Limit': str(expected_rate_limit),
      'Transfer-Encoding': 'chunked',
      'Date': 'Sat, 31 Mar 2018 10:58:09 GMT',
      'Connection': 'keep-alive',
      'Pinterest-Generated-By': '',
    }
    mock_requests.get.return_value = mock_response

    obj = API("abcd1234")
    assert obj.transaction_limit == expected_rate_limit
    mock_requests.get.assert_called_once()


@mock.patch("friendlypins.utils.rest_io.requests")
def test_transaction_remaining(mock_requests):
    mock_response = mock.MagicMock()
    expected_rate_remaining = 10
    mock_response.headers = {
      'Access-Control-Allow-Origin': '*',
      'Age': '0',
      'Cache-Control': 'private',
      'Content-Encoding': 'gzip',
      'Content-Type': 'application/json',
      'Pinterest-Version': 'e3f92ef',
      'X-Content-Type-Options': 'nosniff',
      'X-Pinterest-RID': '12345678',
      'X-Ratelimit-Remaining': str(expected_rate_remaining),
      'Transfer-Encoding': 'chunked',
      'Date': 'Sat, 31 Mar 2018 10:58:09 GMT',
      'Connection': 'keep-alive',
      'Pinterest-Generated-By': '',
    }
    mock_requests.get.return_value = mock_response

    obj = API("abcd1234")
    tmp = obj.transaction_remaining
    mock_requests.get.assert_called_once()
    assert tmp == expected_rate_remaining


@mock.patch("friendlypins.utils.rest_io.requests")
def test_rate_refresh(mock_requests):
    mock_response = mock.MagicMock()
    refresh_time = 30
    start_time_str = 'Sat, 31 Mar 2018 10:58:09 GMT'
    expected_time_str = 'Sat, 31 Mar 2018 10:58:39'

    mock_response.headers = {
      'Access-Control-Allow-Origin': '*',
      'Age': '0',
      'Cache-Control': 'private',
      'Content-Encoding': 'gzip',
      'Content-Type': 'application/json',
      'Pinterest-Version': 'e3f92ef',
      'X-Content-Type-Options': 'nosniff',
      'X-Pinterest-RID': '12345678',
      'Transfer-Encoding': 'chunked',
      'Date': start_time_str,
      'Connection': 'keep-alive',
      'Pinterest-Generated-By': '',
      'X-Ratelimit-Refresh': str(refresh_time)
    }
    mock_requests.get.return_value = mock_response

    obj = API("abcd1234")
    tmp = obj.rate_limit_refresh

    mock_requests.get.assert_called_once()
    tmp = tmp.astimezone(tz.tzutc())
    assert tmp.strftime("%a, %d %b %Y %H:%M:%S") == expected_time_str
