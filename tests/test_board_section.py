import pytest
from friendlypins.api import API
from friendlypins.section import Section
from friendlypins.pin import Pin


@pytest.mark.vcr()
def test_board_sections(test_env):
    obj = API(test_env["key"])
    board = obj.get_board_by_id(test_env["test_board"]["id"])
    sections = list(board.sections)

    assert len(sections) == 1
    assert isinstance(sections[0], Section)
    assert sections[0].unique_id == test_env["test_section"]["id"]
    # TODO: test find_section_by_id and load properties like this
    #assert sections[0].title == test_env["test_section"]["title"]


@pytest.mark.vcr()
@pytest.mark.skip()
def test_section_pins(test_env):
    obj = API(test_env["key"])
    section = obj.get_section_by_id(test_env["test_section"]["id"])
    assert section is not None
    pins = list(section.pins)

    assert len(pins) == len(test_env["test_section"]["pins"])
    for cur_pin in pins:
        assert isinstance(cur_pin, Pin)
        assert cur_pin.unique_id in test_env["test_section"]["pins"]
        test_env["test_section"]["pins"].remove(cur_pin.unique_id)
