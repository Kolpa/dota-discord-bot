import re

import matplotlib
import requests

matplotlib.use('agg')

from agithub.base import API, ConnectionProperties, Client
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from gfycat.client import GfycatClient
import numpy as np


class Opendota(API):
    def __init__(self, *args, **kwargs):
        props = ConnectionProperties(
            api_url='api.opendota.com',
            url_prefix='/api',
            secure_http=True
        )
        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)


dota = Opendota()
gfy = GfycatClient()


async def get_info_for_match(mid):
    status, data = dota.matches[mid].get()
    if status != 200:
        return 'That went wrong'

    return await make_xp_gold_anim(data)


async def make_xp_gold_anim(data):
    golddt = data['radiant_gold_adv']
    xpdt = data['radiant_xp_adv']


    fig = plt.figure()

    plot = fig.add_subplot(111)

    goldx, goldy = [], []
    xpx, xpy = [], []

    goldln, = plt.plot(goldx, goldy, animated=True)
    xpln, = plt.plot(xpx, xpy, animated=True)

    def init():
        plot.set_xlim(0, len(golddt))
        plot.set_ylim(min(golddt + xpdt), max(golddt + xpdt))
        return goldln, xpln

    def update(frame):
        goldx.append(frame)
        goldy.append(golddt[frame])
        goldln.set_data(goldx, goldy)

        xpx.append(frame)
        xpy.append(xpdt[frame])
        xpln.set_data(xpx, xpy)
        return goldln, xpln

    ani = FuncAnimation(fig, update, frames=len(golddt), init_func=init)
    ani.save('test.gif', writer='imagemagick', extra_args=['-deconstruct'], fps=30)

    return 'test.gif'
