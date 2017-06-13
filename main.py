import logging

import asyncio

import SvenReplacer
from discord import ChannelType, Embed
from discord.ext import commands

from modules.github.hero import Type
from modules.github.poller import Dota2Comparator

from modules.info import game_info

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()

client = commands.Bot(loop=loop, command_prefix='!', description='a dota2 info bot')
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


@client.command(pass_context=True)
async def game(ctx, matchid: str):
    await client.send_typing(ctx.message.channel)
    url = await game_info.get_info_for_match(matchid)
    await client.send_file(ctx.message.channel, url)


@client.event
async def on_reaction_add(reaction, user):
    print(reaction, user)
    await client.remove_reaction(reaction.message, reaction.emoji, user)


client.run('***REMOVED***')
