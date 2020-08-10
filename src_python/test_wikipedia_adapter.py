from wikidata_adapter import WikidataAdapter
from wikidata_adapter_v2 import WikidataAdapter_V2

def test_work():
    n = WikidataAdapter('apple')
    assert n.status == 200

def test_work_v2():
    n = WikidataAdapter_V2('apple')
    assert n.status == 200
