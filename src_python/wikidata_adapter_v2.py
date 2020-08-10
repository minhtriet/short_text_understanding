import base_adapter
import json
import aiohttp
import asyncio
import urllib
import itertools
# https://www.wikidata.org/w/api.php?action=query&format=json&prop=pageprops&generator=search&ppprop=wb-claims|wb-sitelinks&gsrsearch=Q89&gsrlimit=1
# https://www.wikidata.org/w/api.php?action=wbsearchentities&search=apple&language=en&limit=20&continue=0&format=json&uselang=en&type=item&origin=*
# https://www.wikidata.org/w/api.php?action=query&list=search&srsearch=harry%20potter&format=json&srlimit=4
class WikidataAdapter_V2(base_adapter.EntityDatabase):

    MAX_RESULTS_NUMBER = base_adapter.EntityDatabase.MAX_RESULTS_NUMBER

    base_url = "https://www.wikidata.org/w/api.php?%s"
    claims_pagelink_dict = {'action': 'query',
                            'prop': 'pageprops',
                            'ppprop': 'wb-claims|wb-sitelinks',
                            'generator': 'search',
                            'format': 'json',
                            'gsrlimit': 1,}
    search_dict = {'action': 'wbsearchentities',
                   'language': 'en',
                   'list': 'search',
                   'limit': 4,
                   'srlimit': MAX_RESULTS_NUMBER,
                   'continue': 0,
                   'format': 'json',
                   'uselang': 'en',
                   'type': 'item',
                   'origin': '*',}
    async def get_info(params_dict, search_key_value):
        params = urllib.parse.urlencode({**params_dict, **search_key_value})
        async with aiohttp.ClientSession() as session:
            async with session.get(WikidataAdapter_V2.base_url % params, ssl=False) as response:
                response_text = await response.text()
            return response.status, json.loads(response_text)

    def __init__(self, entity_name, result_number=MAX_RESULTS_NUMBER):
        search_dict = {'action': 'query',
                   'list': 'search',
                   'srlimit': result_number,
                   'format': 'json',}
        self.entity = entity_name
        self.status, self.json = asyncio.run(WikidataAdapter_V2.get_info(search_dict, {'srsearch': self.entity}))
        self.json = self.json['query']

    async def _get_probabilities(self):
        json_probabilities = [WikidataAdapter_V2.get_info(WikidataAdapter_V2.search_dict,
                                                       {'gsrsearch': json_entity['title']}) for json_entity in self.json['search']]
        results = await asyncio.gather(*json_probabilities)
        return results

    def to_entity_list(self):
        """

        Returns
        -------
        total claims
        detailed dict
        """
        result = asyncio.run(self._get_probabilities())
        if result:  # something is found on wikidata
            statuses, responses = zip(*result)
            responses_dict = [response['query']['pages'].values() for response in responses]
            flattened_responses = list(itertools.chain.from_iterable(responses_dict))
            probabilities_dict = {}
            for flattened_response in flattened_responses:
                probabilities_dict[flattened_response['title']] = float(flattened_response['pageprops']['wb-claims']) + float(flattened_response['pageprops']['wb-sitelinks'])
            denominator = sum([x for x in probabilities_dict.values()])
            entities = [base_adapter.Entity(result['title'],
                                            float(probabilities_dict[result['title']]) / denominator,
                                            result['snippet']) for result in self.json['search'] if result['snippet']]
            return denominator, entities
        return 0, None
