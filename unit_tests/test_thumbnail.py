import pytest
import mock
from friendlypins.thumbnail import Thumbnail

def test_thumbnail_properties():
    expected_url = "https://i.pinimg.com/originals/1/2/3/abcd.jpg"
    expected_width = 800
    expected_height = 600
    data = {
        "original": {
            "url": expected_url,
            "width": str(expected_width),
            "height": str(expected_height)
        }
    }

    obj = Thumbnail(data)

    assert obj.url == expected_url
    assert obj.width == expected_width
    assert obj.height == expected_height

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])