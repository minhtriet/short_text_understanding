import base_adapter
import json
import aiohttp
import asyncio
import urllib
import logging
import itertools
# https://www.wikidata.org/w/api.php?action=query&format=json&prop=pageprops&generator=search&ppprop=wb-claims|wb-sitelinks&gsrsearch=Q89&gsrlimit=1
# https://www.wikidata.org/w/api.php?action=wbsearchentities&search=apple&language=en&limit=20&continue=0&format=json&uselang=en&type=item&origin=*


logging.getLogger("asyncio").setLevel(logging.DEBUG)

class WikidataAdapter(base_adapter.EntityDatabase):
    base_url = "https://www.wikidata.org/w/api.php?%s"
    search_dict = {'action': 'wbsearchentities',
                   'language': 'en',
                   'limit': 4,
                   'continue': 0,
                   'format': 'json',
                   'uselang': 'en',
                   'type': 'item',
                   'origin': '*'}
    claims_pagelink_dict = {'action': 'query',
                            'prop': 'pageprops',
                            'ppprop': 'wb-claims|wb-sitelinks',
                            'generator': 'search',
                            'format': 'json',
                            'gsrlimit': 1}

    async def get_info(params_dict, search_key_value):
        params = urllib.parse.urlencode({**params_dict, **search_key_value})
        async with aiohttp.ClientSession() as session:
            async with session.get(WikidataAdapter.base_url % params, ssl=False) as response:
                response_text = await response.text()
            return response.status, json.loads(response_text)

    def __init__(self, entity_name):
        self.entity = entity_name
        loop = asyncio.get_event_loop()
        self.status, self.json = loop.run_until_complete(WikidataAdapter.get_info(WikidataAdapter.search_dict, {'search': self.entity}))

    def _get_probabilities(self):
        json_probabilities = [WikidataAdapter.get_info(WikidataAdapter.claims_pagelink_dict, {'gsrsearch': json_entity['title']}) for json_entity in self.json['search']]
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(asyncio.gather(*json_probabilities))
        statuses, responses = zip(*result)
        responses_dict = [response['query']['pages'].values() for response in responses]
        flattened_responses = list(itertools.chain.from_iterable(responses_dict))
        probabilities_dict = {}
        for flattened_response in flattened_responses:
            probabilities_dict[flattened_response['title']] = flattened_response['pageprops']['wb-sitelinks']
        return probabilities_dict

    def to_entity_list(self):
        probabilities_dict = self._get_probabilities()
        denominator = sum(probabilities_dict.values()) * 1.
        entities = [base_adapter.Entity(result['title'], 
            probabilities_dict[result['title']] / denominator, result['description'], result['url']) for result in self.json['search']]
        return entities

