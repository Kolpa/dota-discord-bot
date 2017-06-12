import logging

import asyncio

import SvenReplacer

import discord
from discord import ChannelType

from modules.github.hero import Type
from modules.github.poller import Dota2Comparator

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()

client = discord.Client(loop=loop)
poller = Dota2Comparator(loop)


async def say_patch(file, heroes):
    for channel in client.get_all_channels():

        if channel.type == ChannelType.text:
            for hero in heroes:

                msg = 'Changes For {}: \n'.format(hero.name)

                for change in hero.changes:
                    if change.changetype == Type.NEW_PROPERTY:
                        msg += '    {} was added with value {}\n'.format(change.stat, change.new)
                    if change.changetype == Type.CHANGED_PROPERTY:
                        msg += '    {} was change from {} to {}\n'.format(change.stat, change.old, change.new)
                        msg = SvenReplacer.Patchnote_replace(msg)
                await client.send_message(channel, msg[:-1])


poller.on_message += say_patch


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    poller.start()


@client.event
async def on_reaction_add(reaction, user):
    print(reaction, user)
    await client.remove_reaction(reaction.message, reaction.emoji, user)


client.run('***REMOVED***')
