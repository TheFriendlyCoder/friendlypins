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

    obj = Pin(sample_data)

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
    expected_media_type = "video"
    sample_data = {
        "id": str(expected_id),
        "note": expected_note,
        "link": expected_link,
        "url": expected_url,
    }

    obj = Pin(sample_data)

    assert obj.unique_id == expected_id
    assert obj.note == expected_note
    assert obj.url == expected_url
    assert obj.link == expected_link
    assert obj.media_type is None

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])