from wikidata_adapter import WikidataAdapter

def test_apple():
    n = WikidataAdapter('apple')
    assert n.status == 200
    total_probs, entity_list = n.to_entity_list()
    assert len(entity_list) == len(n.json)

