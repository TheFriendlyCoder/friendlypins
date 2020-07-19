import mock
import pytest
from datetime import datetime
from dateutil import tz
from friendlypins.api import API
from friendlypins.board import Board
from friendlypins.user import User


@pytest.mark.vcr()
def test_user_properties(test_env):
    obj = API(test_env["key"])
    user = obj.user
    assert isinstance(user, User)
    assert user.url == test_env["test_user"]["url"]
    assert user.first_name == test_env["test_user"]["first_name"]
    assert user.last_name == test_env["test_user"]["last_name"]
    assert user.name == test_env["test_user"]["full_name"]
    assert user.username == test_env["test_user"]["username"]
    assert user.unique_id == test_env["test_user"]["id"]
    assert isinstance(user.num_boards, int)
    assert isinstance(user.num_pins, int)
    assert isinstance(user.num_followers, int)
    assert user.account_type == test_env["test_user"]["type"]
    assert user.bio == test_env["test_user"]["bio"]
    expected_creation_date = datetime(year=2015, month=3, day=1, hour=2, minute=57, second=37, tzinfo=tz.tzutc())
    assert user.created == expected_creation_date


@pytest.mark.vcr()
def test_get_boards(test_env):
    obj = API(test_env["key"])
    boards = obj.user.boards
    assert boards is not None
    results = list(boards)
    assert all([isinstance(i, Board) for i in results])
    assert any([i.name == test_env["test_board"]["name"] for i in results])


def test_cache_refresh():
    expected_url = 'https://www.pinterest.com/MyUserName/'
    data = {
        'url': expected_url,
    }

    mock_io = mock.MagicMock()
    mock_io.get.return_value = {"data": data}
    obj = User("me", mock_io)
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


def test_create_board():
    expected_name = "My Board"
    expected_desc = "My new board is about this stuff..."
    mock_io = mock.MagicMock()
    mock_io.post.return_value = {
        "data": {
            "name": expected_name,
            "description": expected_desc,
            "id": "12345"
        }
    }
    obj = User("me", mock_io)

    board = obj.create_board(expected_name, expected_desc)
    mock_io.post.assert_called_once()
    assert board is not None
    assert board.name == expected_name
    assert board.description == expected_desc
