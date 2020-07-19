import mock
from friendlypins.board import Board


def test_board_properties():
    expected_id = 1234
    expected_name = "MyBoard"
    expected_url = "https://www.pinterest.ca/MyName/MyBoard/"
    expected_pin_count = 42
    sample_data = {
        "id": str(expected_id),
        "name": expected_name,
        "url": expected_url,
        "counts": {
            "pins": str(expected_pin_count)
        }
    }

    mock_io = mock.MagicMock()
    obj = Board("boards/"+str(expected_id), mock_io, sample_data)
    assert obj.unique_id == expected_id
    assert obj.name == expected_name
    assert obj.url == expected_url
    assert obj.num_pins == expected_pin_count


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


def test_get_pins():
    expected_id = 1234
    expected_url = "https://www.pinterest.ca/MyName/MyPin/"
    expected_note = "My Pin descriptive text"
    expected_link ="http://www.mysite.com/target"
    expected_mediatype = "image"
    expected_data = {
        "data": [{
            "id": str(expected_id),
            "url": expected_url,
            "note": expected_note,
            "link": expected_link,
            "media": {
                "type": expected_mediatype
            }
        }],
        "page": {
            "cursor": None
        }
    }

    mock_io = mock.MagicMock()
    mock_io.get_pages.return_value = [expected_data]
    obj = Board("boards/1234", mock_io)

    result = list()
    for item in obj.pins:
        result.append(item)

    assert len(result) == 1
    assert expected_url == result[0].url
    assert expected_note == result[0].note
    assert expected_id == result[0].unique_id
    assert expected_mediatype == result[0].media_type


def test_delete():
    mock_io = mock.MagicMock()
    expected_url = "boards/1234"
    obj = Board(expected_url, mock_io)
    obj.delete()

    mock_io.delete.assert_called_once_with(expected_url)
