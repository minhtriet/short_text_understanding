from wikidata_adapter import WikidataAdapter

def test_work():
    n = WikidataAdapter('apple')
    assert n.status == 200

