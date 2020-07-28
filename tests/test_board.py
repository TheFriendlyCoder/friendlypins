import mock
import pytest
from friendlypins.api import API
from friendlypins.board import Board
from datetime import datetime
from dateutil import tz


@pytest.mark.vcr()
def test_board_properties(test_env):
    obj = API(test_env["key"])
    board = obj.get_board_by_id(test_env["test_board"]["id"])
    assert board.unique_id == test_env["test_board"]["id"]
    assert board.name == test_env["test_board"]["name"]
    assert board.description == test_env["test_board"]["description"]
    expected_creation_date = datetime(year=2020, month=7, day=21, hour=16, minute=16, second=3, tzinfo=tz.tzutc())
    assert board.creation_date == expected_creation_date
    assert board.privacy_setting == test_env["test_board"]["privacy"]
    assert isinstance(board.num_followers, int)
    assert isinstance(board.num_collaborators, int)
    assert isinstance(board.num_pins, int)
    assert board.num_pins == len(test_env["test_board"]["pins"])


@pytest.mark.vcr()
def test_get_pins(test_env):
    obj = API(test_env["key"])
    board = obj.get_board_by_id(test_env["test_board"]["id"])
    pins = list(board.pins)
    assert len(pins) == len(test_env["test_board"]["pins"])
    for cur_pin in pins:
        assert cur_pin.unique_id in test_env["test_board"]["pins"]
        test_env["test_board"]["pins"].remove(cur_pin.unique_id)


def test_cache_refresh():
    expected_url = 'https://www.pinterest.com/MyUserName/'
    data = {
        'url': expected_url,
    }

    mock_io = mock.MagicMock()
    mock_io.get.return_value = {"data": data}
    obj = Board("boards/1234", mock_io)
    # If we make multiple requests for API data, we should only get
    # a single hit to the remote API endpoint
    assert expected_url == obj.url
    assert expected_url == obj.url
    mock_io.get.assert_called_once()

    # Calling refresh should clear our internal response cache
    # which should not require any additional API calls
    obj.refresh()
    mock_io.get.assert_called_once()

    # Subsequent requests for additional data should reload the cache,
    # and then preserve / reuse the cache data for all subsequent calls,
    # limiting the number of remote requests
    assert expected_url == obj.url
    assert expected_url == obj.url
    assert mock_io.get.call_count == 2


def test_delete():
    mock_io = mock.MagicMock()
    expected_url = "boards/1234"
    obj = Board(expected_url, mock_io)
    obj.delete()

    mock_io.delete.assert_called_once_with(expected_url)
