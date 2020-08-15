import asyncio
import itertools
import wikidata_adapter
import base_adapter

# https://www.wikidata.org/w/api.php?action=query&format=json&prop=pageprops&generator=search&ppprop=wb-claims|wb-sitelinks&gsrsearch=Q89&gsrlimit=1
# https://www.wikidata.org/w/api.php?action=wbsearchentities&search=apple&language=en&limit=20&continue=0&format=json&uselang=en&type=item&origin=*
# https://www.wikidata.org/w/api.php?action=query&list=search&srsearch=harry%20potter&format=json&srlimit=4
class WikidataAdapter_V2(wikidata_adapter.WikidataAdapter):

    MAX_RESULTS_NUMBER = 20

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
        if 'search' not in obj.json or len(obj.json['search']) == 0 or not obj.json['search'][0]['label'].lower().startswith(text):
            return
        # delete disabiguation page
        obj.json['search'] = [ent for ent in obj.json['search'] if 'description' in ent and ent['description'] != 'Wikimedia disambiguation page']
        return obj
    
    def __init__(self, entity_name, result_number=MAX_RESULTS_NUMBER):
        self.entity_name = entity_name

    def to_entity_list(self):
        """
        From the name of the entity, find all possible entity with same name, but different meanings, as well as their count
        Returns
        -------
        total claims
        detailed dict
        """
        results = asyncio.run(self._get_probabilities())
        if results:  # something is found on wikidata
            statuses, responses = zip(*results)
            responses_dict = [response['query']['pages'].values() for response in responses]
            flattened_responses = list(itertools.chain.from_iterable(responses_dict))
            probabilities_dict = {}
            for flattened_response in flattened_responses:
                probabilities_dict[flattened_response['title']] = float(flattened_response['pageprops']['wb-claims']) + float(flattened_response['pageprops']['wb-sitelinks'])
            denominator = sum([x for x in probabilities_dict.values()])
            entities = [base_adapter.Entity(entity['title'],
                                            float(probabilities_dict[entity['title']]) / denominator,
                                            entity['description']) for entity in self.json['search']]
            # only return top 5 most famous
            return denominator, sorted(entities, key=lambda x: x.probability, reverse=True)[:13]
        return 0, None
