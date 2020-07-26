import mock
import pytest
from friendlypins.api import API
from friendlypins.pin import Pin


@pytest.mark.vcr()
def test_pin_properties(test_env):
    obj = API(test_env["key"])
    pin = obj.get_pin_by_id(test_env["test_pin"]["id"])
    assert isinstance(pin, Pin)
    assert pin.unique_id == test_env["test_pin"]["id"]
    assert pin.note == test_env["test_pin"]["note"]
    assert pin.url == test_env["test_pin"]["url"]
    assert pin.link == test_env["test_pin"]["link"]
    assert pin.media_type == test_env["test_pin"]["type"]
    assert pin.thumbnail.url == test_env["test_pin"]["thumbnail_url"]
    assert pin.thumbnail.width == test_env["test_pin"]["thumbnail_width"]
    assert pin.thumbnail.height == test_env["test_pin"]["thumbnail_height"]


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
    obj = Pin("pins/1234", mock_io, sample_data)

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
    obj = Pin("pins/1234", mock_io, data)
    result = obj.thumbnail

    assert result.url == expected_url
