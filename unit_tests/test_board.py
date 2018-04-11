import pytest
import mock
from friendlypins.board import Board

def test_board_properties():
    expected_id = 1234
    expected_name = "MyBoard"
    expected_url = "https://www.pinterest.ca/MyName/MyBoard/"
    sample_data = {
        "id": str(expected_id),
        "name": expected_name,
        "url": expected_url
    }

    obj = Board(sample_data, 'http://pinterest_url', '1234abcd')
    assert obj.unique_id == expected_id
    assert obj.name == expected_name
    assert obj.url == expected_url

def test_get_all_pins():
    data = {
        'id': '987654321'
    }
    api_url = "https://pinterest_url/v1"
    token = "1234abcd"
    obj = Board(data, api_url, token)

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

    with mock.patch("friendlypins.board.requests") as mock_requests:
        mock_response = mock.MagicMock()
        mock_response.json.return_value = expected_data
        mock_requests.get.return_value = mock_response
        result = obj.all_pins

        assert len(result) == 1
        assert expected_url == result[0].url
        assert expected_note == result[0].note
        assert expected_id == result[0].unique_id
        assert expected_mediatype == result[0].media_type
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
