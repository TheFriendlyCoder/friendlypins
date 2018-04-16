import pytest
import mock
import os
from friendlypins.utils.console_actions import download_thumbnails


@mock.patch("friendlypins.utils.console_actions.os")
@mock.patch("friendlypins.utils.console_actions.open")
@mock.patch("friendlypins.utils.console_actions.requests")
@mock.patch("friendlypins.api.RestIO")
def test_download_thumbnails(rest_io, action_requests, mock_open, mock_os):

    # Fake user data for the user authenticating to Pinterest
    expected_user_data = {
        'data': {
            'url': 'https://www.pinterest.com/MyUserName/',
            'first_name': "John",
            'last_name': "Doe",
            'id': "12345678"
        }
    }

    # Fake board data for the boards owned by the fake authenticated user
    expected_board_name = "MyBoard"
    expected_board_data = {
        "data": [{
            "id": "6789",
            "name": expected_board_name,
            "url": "https://www.pinterest.ca/MyName/MyBoard/",
            "counts": {
                "pins": 1
            }
        }]
    }

    # Fake pin data for the fake board, with fake thumbnail metadata
    expected_thumbnail_url = "https://i.pinimg.com/originals/1/2/3/abcd.jpg"
    expected_pin_data = {
        "data": [{
            "id": "1234",
            "url": "https://www.pinterest.ca/MyName/MyPin/",
            "note": "My Pin descriptive text",
            "link": "http://www.mysite.com/target",
            "media": {
                "type": "image"
            },
            "image": {
                "original": {
                    "url": expected_thumbnail_url,
                    "width": "800",
                    "height": "600"
                }
            }
        }],
        "page": {
            "cursor": None
        }
    }

    # fake our Pinterest API data to flex our implementation logic
    mock_response = mock.MagicMock()
    mock_response.get.side_effect = [
        expected_user_data,
        expected_board_data,
        expected_pin_data
        ]
    rest_io.return_value = mock_response

    # Make sure the code think's the output file where the
    # thumbnail is to be downloaded doesn't already exist
    mock_os.path.exists.return_value = False

    # Flex our code
    result = download_thumbnails("1234abcd", expected_board_name, "/tmp", False)

    # Make sure the call was successful, and that our mock APIs
    # that must have executed as part of the process were called
    assert result == 0
    action_requests.get.assert_called_once_with(expected_thumbnail_url, stream=True)
    mock_os.makedirs.assert_called()
    mock_os.path.exists.assert_called()
    mock_open.assert_called()


@mock.patch("friendlypins.utils.console_actions.os")
@mock.patch("friendlypins.utils.console_actions.open")
@mock.patch("friendlypins.utils.console_actions.requests")
@mock.patch("friendlypins.api.RestIO")
def test_download_thumbnails_with_delete(rest_io, action_requests, mock_open, mock_os):

    # Fake user data for the user authenticating to Pinterest
    expected_user_data = {
        'data': {
            'url': 'https://www.pinterest.com/MyUserName/',
            'first_name': "John",
            'last_name': "Doe",
            'id': "12345678"
        }
    }

    # Fake board data for the boards owned by the fake authenticated user
    expected_board_name = "MyBoard"
    expected_board_data = {
        "data": [{
            "id": "6789",
            "name": expected_board_name,
            "url": "https://www.pinterest.ca/MyName/MyBoard/",
            "counts": {
                "pins": 1
            }
        }]
    }

    # Fake pin data for the fake board, with fake thumbnail metadata
    expected_thumbnail_url = "https://i.pinimg.com/originals/1/2/3/abcd.jpg"
    expected_pin_data = {
        "data": [{
            "id": "1234",
            "url": "https://www.pinterest.ca/MyName/MyPin/",
            "note": "My Pin descriptive text",
            "link": "http://www.mysite.com/target",
            "media": {
                "type": "image"
            },
            "image": {
                "original": {
                    "url": expected_thumbnail_url,
                    "width": "800",
                    "height": "600"
                }
            }
        }],
        "page": {
            "cursor": None
        }
    }

    # fake our Pinterest API data to flex our implementation logic
    mock_response = mock.MagicMock()
    mock_response.get.side_effect = [
        expected_user_data,
        expected_board_data,
        expected_pin_data
        ]
    rest_io.return_value = mock_response

    # Make sure the code think's the output file where the
    # thumbnail is to be downloaded doesn't already exist
    mock_os.path.exists.return_value = False

    # Flex our code
    result = download_thumbnails("1234abcd", expected_board_name, "/tmp", True)

    # Make sure the call was successful, and that our mock APIs
    # that must have executed as part of the process were called
    assert result == 0
    action_requests.get.assert_called_once_with(expected_thumbnail_url, stream=True)
    mock_os.makedirs.assert_called()
    mock_os.path.exists.assert_called()
    mock_open.assert_called()
    mock_response.delete.assert_called_once()

@mock.patch("friendlypins.utils.console_actions.os")
@mock.patch("friendlypins.utils.console_actions.open")
@mock.patch("friendlypins.utils.console_actions.requests")
@mock.patch("friendlypins.api.RestIO")
def test_download_thumbnails_error(rest_io, action_requests, mock_open, mock_os):

    # Fake user data for the user authenticating to Pinterest
    expected_user_data = {
        'data': {
            'url': 'https://www.pinterest.com/MyUserName/',
            'first_name': "John",
            'last_name': "Doe",
            'id': "12345678"
        }
    }

    # Fake board data for the boards owned by the fake authenticated user
    expected_board_name = "MyBoard"
    expected_board_data = {
        "data": [{
            "id": "6789",
            "name": expected_board_name,
            "url": "https://www.pinterest.ca/MyName/MyBoard/",
            "counts": {
                "pins": 1
            }
        }]
    }

    # Fake pin data for the fake board, with fake thumbnail metadata
    expected_thumbnail_url = "https://i.pinimg.com/originals/1/2/3/abcd.jpg"
    expected_pin_data = {
        "data": [{
            "id": "1234",
            "url": "https://www.pinterest.ca/MyName/MyPin/",
            "note": "My Pin descriptive text",
            "link": "http://www.mysite.com/target",
            "media": {
                "type": "image"
            },
            "image": {
                "original": {
                    "url": expected_thumbnail_url,
                    "width": "800",
                    "height": "600"
                }
            }
        }],
        "page": {
            "cursor": None
        }
    }

    # fake our Pinterest API data to flex our implementation logic
    mock_response = mock.MagicMock()
    mock_response.get.side_effect = [
        expected_user_data,
        expected_board_data,
        expected_pin_data
        ]
    rest_io.return_value = mock_response

    # Make sure the code think's the output file where the
    # thumbnail is to be downloaded doesn't already exist
    mock_os.path.exists.return_value = False

    # Fake an exception / error condition when downloading our thumbnail
    mock_action_response = mock.MagicMock()
    mock_action_response.raise_for_status.side_effect = Exception('Ooops!')
    action_requests.get.return_value = mock_action_response

    # Flex our code
    result = download_thumbnails("1234abcd", expected_board_name, "/tmp", False)

    # Make sure the call was successful, and that our mock APIs
    # that must have executed as part of the process were called
    assert result != 0
    action_requests.get.assert_called_once_with(expected_thumbnail_url, stream=True)
    mock_os.makedirs.assert_called()
    mock_os.path.exists.assert_called()
    assert not mock_open.called

@mock.patch("friendlypins.utils.console_actions.os")
@mock.patch("friendlypins.utils.console_actions.open")
@mock.patch("friendlypins.utils.console_actions.requests")
@mock.patch("friendlypins.api.RestIO")
def test_download_thumbnails_missing_board(rest_io, action_requests, mock_open, mock_os):

    # Fake user data for the user authenticating to Pinterest
    expected_user_data = {
        'data': {
            'url': 'https://www.pinterest.com/MyUserName/',
            'first_name': "John",
            'last_name': "Doe",
            'id': "12345678"
        }
    }

    # Fake board data for the boards owned by the fake authenticated user
    expected_board_data = {
        "data": [{
            "id": "6789",
            "name": "MyBoard",
            "url": "https://www.pinterest.ca/MyName/MyBoard/",
            "counts": {
                "pins": 1
            }
        }]
    }

    # Fake pin data for the fake board, with fake thumbnail metadata
    expected_thumbnail_url = "https://i.pinimg.com/originals/1/2/3/abcd.jpg"
    expected_pin_data = {
        "data": [{
            "id": "1234",
            "url": "https://www.pinterest.ca/MyName/MyPin/",
            "note": "My Pin descriptive text",
            "link": "http://www.mysite.com/target",
            "media": {
                "type": "image"
            },
            "image": {
                "original": {
                    "url": expected_thumbnail_url,
                    "width": "800",
                    "height": "600"
                }
            }
        }],
        "page": {
            "cursor": None
        }
    }

    # fake our Pinterest API data to flex our implementation logic
    mock_response = mock.MagicMock()
    mock_response.get.side_effect = [
        expected_user_data,
        expected_board_data,
        expected_pin_data
        ]
    rest_io.return_value = mock_response

    # Make sure the code think's the output file where the
    # thumbnail is to be downloaded doesn't already exist
    mock_os.path.exists.return_value = False

    # Flex our code
    result = download_thumbnails("1234abcd", "FuBar", "/tmp", False)

    # Make sure the call was successful, and that our mock APIs
    # that must have executed as part of the process were called
    assert result != 0
    assert not action_requests.get.called
    assert not mock_os.makedirs.called
    assert not mock_os.path.exists.called
    assert not mock_open.called

@mock.patch("friendlypins.utils.console_actions.os")
@mock.patch("friendlypins.utils.console_actions.open")
@mock.patch("friendlypins.utils.console_actions.requests")
@mock.patch("friendlypins.api.RestIO")
def test_download_thumbnails_exists(rest_io, action_requests, mock_open, mock_os):

    # Fake user data for the user authenticating to Pinterest
    expected_user_data = {
        'data': {
            'url': 'https://www.pinterest.com/MyUserName/',
            'first_name': "John",
            'last_name': "Doe",
            'id': "12345678"
        }
    }

    # Fake board data for the boards owned by the fake authenticated user
    expected_board_name = "MyBoard"
    expected_board_data = {
        "data": [{
            "id": "6789",
            "name": expected_board_name,
            "url": "https://www.pinterest.ca/MyName/MyBoard/",
            "counts": {
                "pins": 1
            }
        }]
    }

    # Fake pin data for the fake board, with fake thumbnail metadata
    expected_filename = "abcd.jpg"
    expected_thumbnail_url = "https://i.pinimg.com/originals/1/2/3/" + expected_filename
    expected_pin_data = {
        "data": [{
            "id": "1234",
            "url": "https://www.pinterest.ca/MyName/MyPin/",
            "note": "My Pin descriptive text",
            "link": "http://www.mysite.com/target",
            "media": {
                "type": "image"
            },
            "image": {
                "original": {
                    "url": expected_thumbnail_url,
                    "width": "800",
                    "height": "600"
                }
            }
        }],
        "page": {
            "cursor": None
        }
    }

    # fake our Pinterest API data to flex our implementation logic
    mock_response = mock.MagicMock()
    mock_response.get.side_effect = [
        expected_user_data,
        expected_board_data,
        expected_pin_data
        ]
    rest_io.return_value = mock_response

    # Make sure the code think's the output file where the
    # thumbnail is to be downloaded exists already
    mock_os.path.exists.return_value = True
    mock_os.path.join = os.path.join
    mock_os.path.basename = os.path.basename

    # Flex our code
    output_folder = "/tmp"
    result = download_thumbnails("1234abcd", expected_board_name, output_folder, False)

    # Make sure the call was successful, and that our mock APIs
    # that must have executed as part of the process were called
    assert result == 0
    assert not action_requests.get.called
    assert not mock_os.makedirs.called
    mock_os.path.exists.assert_called_with(os.path.join(output_folder, expected_filename))
    assert not mock_open.called


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])