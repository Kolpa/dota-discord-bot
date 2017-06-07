import json
from json import JSONEncoder
from threading import Thread
from configparser import ConfigParser

import asyncio
from agithub.GitHub import GitHub
from modules.events import EventHandler, AsyncEventHandler
from requests import get
from keyvalues import KeyValues
import time

from modules.github.hero import Hero, Change, Type

git = GitHub()


class GithubWorker(Thread):
    def __init__(self, interval, files):
        Thread.__init__(self)
        self.interval = interval
        self.runme = True
        self.files = files
        self.on_data = EventHandler(self)

    def run(self):
        while self.runme:
            print("Github is now being polled")
            for file in self.files:
                status, data = git.repos['SteamDatabase']['GameTracking-Dota2'].commits.get(path=file)
                if status == 200:
                    print('checking {}'.format(file))
                    self.on_data(file, data)

            time.sleep(self.interval)

    def stop(self):
        self.runme = False


class CommitManager:
    def __init__(self, files):
        self.files = files
        self.local = ConfigParser()
        self.__init_config()

    def __init_config(self):
        self.local.read('local-git.ini')

        if not self.local.has_section('local'):
            self.local.add_section('local')
            for file in self.files:
                self.set_local_version(file, '-1')

    def __write_config(self):
        with open('local-git.ini', 'w') as fh:
            self.local.write(fh)

    def get_local_version(self, file):
        sha = self.local.get('local', file)
        return sha

    def set_local_version(self, name, sha):
        self.local.set('local', name, sha)
        self.__write_config()


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Dota2Comparator:
    def __init__(self, loop):
        self.loop = loop

        self.tracked_files = ['game/dota/scripts/npc/npc_heroes.txt']
        self.checkers = [self.compare_hero_kv_data]

        self.manager = CommitManager(self.tracked_files)

        self.poller = GithubWorker(60, self.tracked_files)
        self.poller.on_data += self.handle_commits

        self.on_message = AsyncEventHandler(self)

    def handle_commits(self, file, data):
        old_sha = self.manager.get_local_version(file)
        if old_sha != data[0]['sha']:
            print('got new Commit')
            self.handle_update(file, old_sha, data)

    def __build_raw_url(self, sha, file):
        return 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-Dota2/{0}/{1}'.format(sha, file)

    def handle_update(self, file, old_sha, data):
        new_sha = data[0]['sha']

        print(old_sha + ' vs ' + new_sha)

        if old_sha == '-1':
            old_sha = data[-1]['sha']

        print('previous old version is {}'.format(old_sha))
        self.manager.set_local_version(file, new_sha)

        print(self.__build_raw_url(new_sha, file))

        new_data = get(self.__build_raw_url(new_sha, file)).text
        old_data = get(self.__build_raw_url(old_sha, file)).text

        message = self.checkers[self.tracked_files.index(file)](new_data, old_data)

        self.loop.call_soon_threadsafe(asyncio.async, self.on_message(file, message))

    def compare_hero_kv_data(self, new_data, old_data):
        new_kv = KeyValues()
        old_kv = KeyValues()

        new_kv.loads(new_data)
        old_kv.loads(old_data)

        diff_list = []

        for hero in new_kv:
            if hero == 'Version':
                continue

            outh = Hero(hero)

            if hero in old_kv:
                for stat in new_kv[hero]:
                    if type(new_kv[hero][stat]) != str:
                        continue

                    if stat in old_kv[hero]:
                        if new_kv[hero][stat] != old_kv[hero][stat]:
                            outh.add_change(Change(stat, old_kv[hero][stat], new_kv[hero][stat], Type.CHANGED_PROPERTY))
                    else:
                        outh.add_change(Change(stat, None, new_kv[hero][stat], Type.NEW_PROPERTY))
            else:
                for stat in new_kv[hero]:
                    if type(new_kv[hero][stat]) != str:
                        continue

                    outh.add_change(Change(stat, None, new_kv[hero][stat], Type.NEW_PROPERTY))

            if outh.has_changes():
                diff_list.append(outh)

        return diff_list

    def start(self):
        self.poller.start()
