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
    obj = User(data, mock_io)
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
    obj = User(data, mock_io)

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
    data = {
        "id": "1234",
        "first_name": "Jonh",
        "last_name": "Doe"
    }
    mock_io = mock.MagicMock()
    mock_io.post.return_value = {
        "data": {
            "name": expected_name,
            "description": expected_desc,
            "id": "12345"
        }
    }
    obj = User(data, mock_io)

    board = obj.create_board(expected_name, expected_desc)
    mock_io.post.assert_called_once()
    assert board is not None
    assert board.name == expected_name
    assert board.description == expected_desc
