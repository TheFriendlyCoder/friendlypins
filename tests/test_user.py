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

    mock_io = mock.MagicMock()
    mock_io.get.return_value = {"data": data}
    obj = User("me", mock_io)
    assert expected_url == obj.url
    assert expected_firstname == obj.first_name
    assert expected_lastname == obj.last_name
    assert expected_id == obj.unique_id
    assert expected_board_count == obj.num_boards
    assert expected_pin_count == obj.num_pins
    mock_io.get.assert_called_once()


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


def test_get_boards():
    expected_id = 1234
    expected_name = "MyBoard"
    expected_url = "https://www.pinterest.ca/MyName/MyBoard/"
    expected_data = {
        "data": [{
            "id": str(expected_id),
            "name": expected_name,
            "url": expected_url
        }],
        "page": {
            "cursor": None
        }
    }

    mock_io = mock.MagicMock()
    mock_io.get_pages.return_value = [expected_data]
    obj = User("me", mock_io)

    result = list()
    for item in obj.boards:
        result.append(item)

    assert len(result) == 1
    assert expected_url == result[0].url
    assert expected_name == result[0].name
    assert expected_id == result[0].unique_id


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
