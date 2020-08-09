import nerd
import pytest

def test_one_entity():
    result = nerd.disambiguate("read harry potter")
    assert len(result) == 1
    assert result[0].name == 'Q8337'  # Harry Potter the series

def test_one_entity_with_noise():
    result = nerd.disambiguate("thick harry potter book")
    assert len(result) == 1
    assert result[0].name == 'Q3244512'  # Harry Potter the character
    # Q3244512, interestingly, not Q8337 because thick series book seems nonsense

def test_another_entity():
    result = nerd.disambiguate("watch harry potter")
    assert len(result) == 1
    assert result[0].name == 'Q216930'  # Harry Potter the film

def test_consistency():
    result_0 = nerd.disambiguate("read harry potter")
    result_1 = nerd.disambiguate("watch harry potter")
    result = nerd.disambiguate("read harry potter vs watch harry potter")
    assert len(result) == 2
    assert result[0].name == result_0[0].name and result[1].name == result_1[0].name


def test_long_entity()
    result = nerd.disambiguate('rage against the machine');
    assert result[0].name == 'Q72092'

