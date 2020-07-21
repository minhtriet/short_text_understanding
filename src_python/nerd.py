import aiohttp
import asyncio
import urllib
# https://www.wikidata.org/w/api.php?action=wbsearchentities&search=apple&language=en&limit=20&continue=0&format=json&uselang=en&type=item&origin=*

class NERD:
    
    base_url = "https://www.wikidata.org/w/api.php?%s"
    params_dict = {'action': 'wbsearchentities', 
            'language': 'en', 
            'limit': 4, 
            'continue': 0, 
            'format': 'json', 
            'uselang': 'en', 
            'type': 'item', 
            'origin': '*'}


    async def get_info(query):
        params = urllib.parse.urlencode({**NERD.params_dict, 'search': query})
        async with aiohttp.ClientSession() as session:
            async with session.get(NERD.base_url % params, ssl=False) as response:
                json = await response.text()
            return response.status, json


    def __init__(self, name):
        loop = asyncio.get_event_loop()
        self.status, self.json = loop.run_until_complete(NERD.get_info(name))


    def disambiguate(self, before, after):
        pass
        

