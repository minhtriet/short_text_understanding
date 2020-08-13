import asyncio

import wikidata_adapter


# https://www.wikidata.org/w/api.php?action=query&format=json&prop=pageprops&generator=search&ppprop=wb-claims|wb-sitelinks&gsrsearch=Q89&gsrlimit=1
# https://www.wikidata.org/w/api.php?action=wbsearchentities&search=apple&language=en&limit=20&continue=0&format=json&uselang=en&type=item&origin=*
# https://www.wikidata.org/w/api.php?action=query&list=search&srsearch=harry%20potter&format=json&srlimit=4
class WikidataAdapter_V2(wikidata_adapter.WikidataAdapter):

    MAX_RESULTS_NUMBER = wikidata_adapter.WikidataAdapter.MAX_RESULTS_NUMBER

    search_dict = {'action': 'wbsearchentities',
                   'language': 'en',
                   'limit': MAX_RESULTS_NUMBER,
                   'continue': 0,
                   'format': 'json',
                   'uselang': 'en',
                   'type': 'item',
                   'origin': '*',}

    def __new__(cls, text):
        obj = super(WikidataAdapter_V2, cls).__new__(cls)
        obj.status, obj.json = asyncio.run(WikidataAdapter_V2.get_info(WikidataAdapter_V2.search_dict, {'search': text}))
        if not obj.json['search'] or not obj.json['search'][0]['label'].lower().startswith(text):
            return
        return obj
    
    def __init__(self, entity_name, result_number=MAX_RESULTS_NUMBER):
        self.entity = entity_name

