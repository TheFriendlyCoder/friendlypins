import pytest
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
    obj = Board(sample_data, mock_io)
    assert obj.unique_id == expected_id
    assert obj.name == expected_name
    assert obj.url == expected_url
    assert obj.num_pins == expected_pin_count


def test_get_all_pins():
    data = {
        'id': '987654321',
        'name': 'MyBoard'
    }

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
    mock_io.get.return_value = expected_data
    obj = Board(data, mock_io)

    result = obj.all_pins

    assert len(result) == 1
    assert expected_url == result[0].url
    assert expected_note == result[0].note
    assert expected_id == result[0].unique_id
    assert expected_mediatype == result[0].media_type


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
