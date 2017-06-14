import aiohttp
from requests import get
from os.path import isfile, exists
from os import makedirs
from PIL import Image


class Hero:
    tranlator = get('https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v1/?key'
                    '=C9C18C12441596E2E97EDB542766BD52&language=de_de').json()
    cachepath = 'cache/heroes/'

    if not exists(cachepath):
        makedirs(cachepath)

    def __init__(self):
        self.name = ""
        self.icon = ""
        self.items = []

    @staticmethod
    async def create(hid):
        hr = Hero()

        hr.name = await Hero.__get_name_by_id(hid)
        hr.icon = await Hero.__get_icon_by_name(hr.name)
        hr.items = []

        return hr

    @staticmethod
    async def __get_icon_by_name(name):
        icon = await Hero.__get_icon_from_cache(name)

        if not icon:
            icon = await Hero.__write_file_to_cache(name)

        return icon

    @staticmethod
    async def __write_file_to_cache(name):

        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.opendota.com/apps/dota2/images/heroes/{}_full.png'.format(name)) as resp:

                if resp.status == 200:
                    with open(Hero.cachepath + name, 'wb') as fd:

                        while True:
                            chunk = await resp.content.read(1024)
                            if not chunk:
                                break
                            fd.write(chunk)

                    return Image.open(Hero.cachepath + name)

                return None

    @staticmethod
    async def __get_icon_from_cache(name):
        if isfile(Hero.cachepath + name):
            return Image.open(Hero.cachepath + name)

        return None

    @staticmethod
    async def __get_name_by_id(id):
        heroes = Hero.tranlator['result']['heroes']

        for hero in heroes:
            if hero['id'] == id:
                return hero['name'].replace('npc_dota_hero_', '')
        return None
