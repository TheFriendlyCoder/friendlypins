import mock
from friendlypins.pin import Pin


def test_pin_properties():
    expected_id = 1234
    expected_note = "Here's my note"
    expected_url = "https://www.pinterest.ca/MyName/MyPin/"
    expected_link = "http://www.google.ca"
    expected_media_type = "video"
    sample_data = {
        "id": str(expected_id),
        "note": expected_note,
        "link": expected_link,
        "url": expected_url,
        "media": {
            "type": expected_media_type
        }
    }

    mock_io = mock.MagicMock()
    obj = Pin(sample_data, mock_io)

    assert obj.unique_id == expected_id
    assert obj.note == expected_note
    assert obj.url == expected_url
    assert obj.link == expected_link
    assert obj.media_type == expected_media_type


def test_pin_missing_media_type():
    expected_id = 1234
    expected_note = "Here's my note"
    expected_url = "https://www.pinterest.ca/MyName/MyPin/"
    expected_link = "http://www.google.ca"
    sample_data = {
        "id": str(expected_id),
        "note": expected_note,
        "link": expected_link,
        "url": expected_url,
    }

    mock_io = mock.MagicMock()
    obj = Pin(sample_data, mock_io)

    assert obj.unique_id == expected_id
    assert obj.note == expected_note
    assert obj.url == expected_url
    assert obj.link == expected_link
    assert obj.media_type is None


def test_delete():
    data = {
        "id": "12345678",
        "note": "My Pin Description"
    }

    mock_io = mock.MagicMock()
    obj = Pin(data, mock_io)
    obj.delete()

    mock_io.delete.assert_called_once()


def test_get_thumbnail():
    expected_url = "https://i.pinimg.com/r/pin/12345"
    data = {
        "image": {
            "original": {
                "url": expected_url
            }
        }
    }

    mock_io = mock.MagicMock()
    obj = Pin(data, mock_io)
    result = obj.thumbnail

    assert result.url == expected_url
