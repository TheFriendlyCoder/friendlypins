import pytest
from friendlypins.api import API
from friendlypins.section import Section
from friendlypins.pin import Pin


@pytest.mark.vcr()
#@pytest.mark.skip(reason="need to retest with additional fields property")
def test_board_sections(test_env):
    obj = API(test_env["key"])
    board = obj.get_board_by_id(test_env["test_board"]["id"])
    sections = list(board.sections)

    assert len(sections) == 1
    assert isinstance(sections[0], Section)


@pytest.mark.vcr()
@pytest.mark.skip(reason="Failing with 405 for some reason")
def test_section_properties(test_env):
    obj = API(test_env["key"])
    #board = obj.get_board_by_id(test_env["test_board"]["id"])
    section = obj.get_section_by_id(test_env["test_section"]["id"])
    #section = board.get_section_by_id(test_env["test_section"]["id"])

    assert isinstance(section, Section)
    assert section.unique_id == test_env["test_section"]["id"]
    assert section.title == test_env["test_section"]["title"]


@pytest.mark.vcr()
def test_create_section(test_env):
    obj = API(test_env["key"])
    board = obj.get_board_by_id(test_env["test_board"]["id"])
    section = board.create_section("My Cool Title")
    assert isinstance(section, Section)


@pytest.mark.vcr()
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
