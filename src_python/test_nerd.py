import nerd
import pytest

@pytest.mark.parametrize("test_input,expected_len,expected_entity", 
    [("and", 0, None),
      ("read harry potter", 1, "Q8837"),
      ('thick harry potter book', 1, 'Q3244512'),   # Q3244512, not Q8337, because thick series book seems nonsense
      ("watch harry potter", 1, "Q216930"),
      ('rage against the machine', 1, 'Q72092'),])
def test_one_entity(test_input, expected_len, expected_entity):
    result = nerd.disambiguate(test_input)
    if not expected_entity:
        assert 'error' in result[0].keys
    else:
        assert len(result) == expected_len
        assert result[0]['name'] == expected_entity

def test_consistency():
    result_0 = nerd.disambiguate("read harry potter")
    result_1 = nerd.disambiguate("watch harry potter")
    result = nerd.disambiguate("read harry potter vs watch harry potter")
    assert len(result) == 2
    assert result[0].name == result_0[0].name and result[1].name == result_1[0].name


