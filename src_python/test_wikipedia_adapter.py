from wikidata_adapter import WikidataAdapter

def test_apple():
    n = WikidataAdapter('apple')
    assert n.status == 200
    prob_dicts = n.get_probabilities()
    assert len(prob_dicts.keys()) == len(n.json)

