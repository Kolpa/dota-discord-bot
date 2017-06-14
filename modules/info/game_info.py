import matplotlib
from io import BytesIO

from PIL import Image

matplotlib.use('agg')

from agithub.base import API, ConnectionProperties, Client
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from modules.info.hero import Hero
from modules.info.item import Item


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


async def get_info_for_match(mid):
    status, data = dota.matches[mid].get()
    if status != 200:
        return 'That went wrong'

    return data

async def sort_players(data):
    radiant = []
    dire = []

    for player in data['players']:
        hero = await Hero.create(player['hero_id'])
        for itemstr in ['item_{}'.format(i) for i in range(6)]:
            if player[itemstr] != 0:
                hero.items.append(await Item.create(player[itemstr]))

        if player['isRadiant']:
            radiant.append(hero)
        else:
            dire.append(hero)

    return radiant, dire

async def make_item_anim(data):
    radiant, dire = await sort_players(data)

    hero_height = 50
    hero_width = 100

    item_height = 25
    item_width = 50

    height = len(radiant + dire) * hero_height + 30

    outim = Image.new('RGBA', (hero_width + item_width * 6, height))

    lastof = 0

    for ind, hero in enumerate(radiant):
        newhim = hero.icon.copy().resize((hero_width, hero_height))
        outim.paste(newhim, (0, ind * hero_height))
        for iind, item in enumerate(hero.items):
            newiim = item.icon.copy().resize((item_width, item_height))
            outim.paste(newiim, (hero_width + iind * item_width, ind * hero_height + 15))

        lastof = ind * hero_height + hero_height

    for ind, hero in enumerate(dire):
        newim = hero.icon.copy().resize((hero_width, hero_height))
        outim.paste(newim, (0, ind * hero_height + 30 + lastof))
        for iind, item in enumerate(hero.items):
            newiim = item.icon.copy().resize((item_width, item_height))
            outim.paste(newiim, (hero_width + iind * item_width, ind * hero_height + 30 + lastof + 15))

    outfile = BytesIO()
    outfile.name = 'test.png'

    outim.save(outfile, format='png')

    outfile.flush()
    outfile.seek(0)

    return outfile

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
    ani.save('test.gif', writer='imagemagick', extra_args=['-deconstruct'], fps=60)

    return 'test.gif'
