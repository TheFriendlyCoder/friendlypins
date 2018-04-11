import pytest
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

    obj = Board(sample_data)
    assert obj.unique_id == expected_id
    assert obj.name == expected_name
    assert obj.url == expected_url

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
