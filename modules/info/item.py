import aiohttp
from requests import get
from os.path import isfile, exists
from os import makedirs
from PIL import Image


class Item:
    tranlator = get('http://api.steampowered.com/IEconDOTA2_570/GetGameItems/v1'
                    '?key=C9C18C12441596E2E97EDB542766BD52&language=de_de').json()

    cachepath = 'cache/items/'

    if not exists(cachepath):
        makedirs(cachepath)

    def __init__(self):
        self.name = ""
        self.icon = None

    @staticmethod
    async def create(id):
        it = Item()
        it.name = await Item.__get_name_by_id(id)
        it.icon = await Item.__get_icon_by_name(it.name)

        return it

    @staticmethod
    async def __get_icon_by_name(name):
        icon = await Item.__get_icon_from_cache(name)

        if not icon:
            icon = await Item.__write_file_to_cache(name)

        return icon

    @staticmethod
    async def __write_file_to_cache(name):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.opendota.com/apps/dota2/images/items/{}_lg.png'.format(name)) as resp:

                if resp.status == 200:
                    with open(Item.cachepath + name, 'wb') as fd:

                        while True:
                            chunk = await resp.content.read(1024)
                            if not chunk:
                                break
                            fd.write(chunk)

                    return Image.open(Item.cachepath + name)

                return None

    @staticmethod
    async def __get_icon_from_cache(name):
        if isfile(Item.cachepath + name):
            return Image.open(Item.cachepath + name)

        return None

    @staticmethod
    async def __get_name_by_id(id):
        items = Item.tranlator['result']['items']

        for item in items:
            if item['id'] == id:
                return item['name'].replace('item_', '')

        return None