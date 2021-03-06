import logging

import asyncio

import Voice_bot
from gtts import gTTS

import SvenReplacer
from discord import File, TextChannel, FFmpegPCMAudio
from discord.ext import commands

from modules.github.hero import Type
from modules.github.poller import Dota2Comparator

from modules.info import game_info

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()

client = commands.Bot(loop=loop, command_prefix='!', description='a dota2 info bot')
poller = Dota2Comparator(loop)

Voice_bot.VoiceBot.voice = None


async def say_patch(file, heroes):
    for channel in client.get_all_channels():

        if isinstance(channel, TextChannel):
            for hero in heroes:

                msg = 'Changes For {}: \n'.format(hero.name)

                for change in hero.changes:
                    if change.changetype == Type.NEW_PROPERTY:
                        msg += '    {} was added with value {}\n'.format(change.stat, change.new)
                    if change.changetype == Type.CHANGED_PROPERTY:
                        msg += '    {} was change from {} to {}\n'.format(change.stat, change.old, change.new)
                        msg = SvenReplacer.SvenReplacer.Patchnote_replace(msg)
                await channel.send(msg[:-1])


poller.on_message += say_patch


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    poller.start()


@client.command()
async def game(ctx, matchid: str):
    async with ctx.typing():
        data = await game_info.get_info_for_match(matchid)
        items = await game_info.make_item_anim(data)
        gpm = await game_info.make_xp_gold_anim(data)
        await ctx.send('Match ' + matchid, files=[File(gpm), File(items)])
        
#Ansager für Voicechannel beitritt        
@client.event
async def on_voice_state_update(member, before, after):
    if Voice_bot.VoiceBot.voice is None:
        channel = client.get_channel(211042061959299072)
        Voice_bot.VoiceBot.voice = await channel.connect()

    print(before)
    print(after)
    before = str(before)
    bef = before.split()
    after = str(after)
    aft = after.split()
    name = member.nick

    if member.nick is None:         #entfernt die ID nummer in der Ansage wenn kein nickname gesetzt ist
        name = str(member)
        name = name.replace('#', ' ')
        words = name.split()
        name = name.replace(words[-1], ' ')

    if before.__contains__('channel=None'):
        text_to_speech = gTTS(text=name + "hat den channel betreten.", lang='de', slow=False)  # text to speech
        text_to_speech.save("member.mp3")  # test
        print(name + 'betreten')  # console debug
        play_voicestate()

    if after.__contains__('channel=None'):
        text_to_speech = gTTS(text=name + "hat den channel verlassen.", lang='de', slow=False)  # text to speech
        text_to_speech.save("member.mp3")  # test
        print(name + 'verlassen')  # console debug
        play_voicestate()

    #Channel wechseln
    if after.count(' ') == 6:
        if not aft[6] == bef[6] and not aft[6] == 'name=None' and not bef[6] == 'name=None':
            text_to_speech = gTTS(text=name + "hat den channel gewechselt.", lang='de', slow=False)  # text to speech
            text_to_speech.save("member.mp3")  # test
            print(name + 'gewechselt')  # console debug
            play_voicestate()

           
def play_voicestate():
    audio = FFmpegPCMAudio("member.mp3")
    Voice_bot.VoiceBot.voice.play(audio)

client.run('MjQzNDQ3MjM4MDk1Nzk4Mjc0.DA9JOA.F3mT67ZeQ_Pj80MaQPv2vtHwRPs')
