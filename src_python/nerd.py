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

    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def get_info(query):
        async with aiohttp.ClientSession() as session:
            params = urllib.parse.urlencode({**NERD.params_dict, 'search': query})
            html = await NERD.fetch(session, NERD.base_url % params)
            import pdb; pdb.set_trace()
            print(html)


    def __init__(self, name):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(NERD.get_info(name))
