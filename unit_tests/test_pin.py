import pytest
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

    obj = Pin(sample_data, "http://www.pinterest.com", "1234abcd")

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

    obj = Pin(sample_data, "http://www.pinterest.com", "1234abcd")

    assert obj.unique_id == expected_id
    assert obj.note == expected_note
    assert obj.url == expected_url
    assert obj.link == expected_link
    assert obj.media_type is None

def test_delete():
    api_url = "https://pinterest_url/v1"
    token = "1234abcd"

    data = {
        "id": "12345678"
    }

    obj = Pin(data, api_url, token)

    with mock.patch("friendlypins.pin.requests") as mock_requests:
        mock_response = mock.MagicMock()
        mock_requests.delete.return_value = mock_response

        obj.delete()
        mock_requests.delete.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

def test_get_thumbnail():
    expected_url = "https://i.pinimg.com/r/pin/12345"
    data = {
        "image": {
            "original": {
                "url": expected_url
            }
        }
    }

    obj = Pin(data, "http://www.pinterest.com", "1234abcd")
    result = obj.thumbnail

    assert result.url == expected_url
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])