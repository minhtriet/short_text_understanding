import nerd
import pytest

@pytest.mark.skip(reason="done")
def test_one_entity():
    result = nerd.disambiguate("read harry potter")
    assert len(result) == 1
    assert result[0].name == 'Q8337'  # Harry Potter the book

def test_another_entity():
    result = nerd.disambiguate("watch harry potter")
    assert len(result) == 1

@pytest.mark.skip(reason="done")
def test_multiple_entities():
    result = nerd.disambiguate("read harry potter vs watch harry potter")
    assert len(result) == 2

@pytest.mark.skip(reason="done")
def test_consistency():
    result_0 = nerd.disambiguate("read harry potter")
    result_1 = nerd.disambiguate("watch harry potter")
    result = nerd.disambiguate("read harry potter vs watch harry potter")
    assert result[0].name == result_0[0].name and result[1].name == result_1[0].name
