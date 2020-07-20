import aiohttp
import asyncio

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
            params = urllib.parse.urlencode({**params_dict, 'search': query})
            html = await fetch(session, base_url % params)
            import pdb; pdb.set_trace()
            print(html)


    def __init__(name):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_info(name))
