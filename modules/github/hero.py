from enum import Enum
from requests import get


class Type(Enum):
    NEW_PROPERTY = 0
    CHANGED_PROPERTY = 1


class Hero:
    tranlator = get('https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?key'
                    '=C9C18C12441596E2E97EDB542766BD52&language=de_de').json()

    def __init__(self, name):
        self.name = Hero.__translate_name(name)
        self.changes = []

    @staticmethod
    def __translate_name(name):
        heroes = Hero.tranlator['result']['heroes']

        for hero in heroes:
            if hero['name'] == name:
                return hero['localized_name']

        return None

    def add_change(self, change):
        self.changes.append(change)

    def has_changes(self):
        return len(self.changes) > 0


class Change:
    def __init__(self, stat, old, new, changetype):
        self.stat = stat
        self.old = old
        self.new = new
        self.changetype = changetype
