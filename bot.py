# bot.py
import os

import calcCosts
import calcWAR
import util
import disnake
from collections import OrderedDict
from dotenv import load_dotenv
from disnake.ext import commands
from statistics import median
from typing import Optional

PREFIX = '.'

load_dotenv()
API_URL = "https://osu.ppy.sh/api/"
TOKEN = os.getenv('DISCORD_TOKEN') # put these in your own .env
OSU_KEY = os.getenv('OSU_API_KEY')  

intents = disnake.Intents.default()
intents.message_content = True  
bot = commands.InteractionBot(test_guilds=[494563273006645248])  # replace with your own server

# Initialization message.
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
# Rank command
@bot.slash_command(description="Gets a player's osu! rank")
async def rank(inter, user: str):
    rank = util.get_rank(OSU_KEY, user, API_URL)
    properUser = util.user_from_id(OSU_KEY, user, API_URL)
    await inter.response.send_message(properUser + " is rank " + rank + "!")

# Strict RWS Calculation
@bot.slash_command(description="[DEPRECATED] Calculates strict wins above replacement")
async def match_rws(inter, matchurl: str):
    await inter.response.defer()
    id = matchurl.split('/')
    id = id[len(id) - 1]
    maps = util.getMaps(OSU_KEY, id, API_URL)
    maps = calcCosts.parseMaps(maps)
    costs = {}
    for key in maps:
        mapCosts = calcCosts.costsWrapper(OSU_KEY, maps[key], API_URL) 
        for player in mapCosts:
            if player not in costs:
                costs[player] = 0
            costs[player] += mapCosts[player]
    costArr = [playerCost for playerCost in costs.values()]
    medianCost = median(costArr)
    for player in costs:
        costs[player] /= medianCost
    await inter.edit_original_response(costs)

# Adjusted WAR calculation
@bot.slash_command(description="Calculates wins above replacement using a Monte Carlo simulation.")
async def osu_war(inter, matchurl: str, warmups: Optional[int] = 0, ignore_from_end: Optional[int] = 0):
    await inter.response.defer()
    id = matchurl.split('/')
    id = id[len(id) - 1]
    maps = util.getMaps(OSU_KEY, id, API_URL)
    maps = maps[warmups:len(maps) - ignore_from_end]
    result, blue = calcWAR.war_wrapper(maps, OSU_KEY, API_URL)

    embed = disnake.Embed(
    title=util.getMatchName(OSU_KEY, id, API_URL),
    )
    sort = sorted(result.items(), key=lambda item: item[1], reverse=True)
    top_id = util.id_from_user(OSU_KEY, sort[0][0], API_URL)
    tops = [tup[0] for tup in sort[:3]]
    sortD = dict(sort)

    teams = False
    if len(blue) != 0:
        teams = True

    for player in sortD:
        name = player
        if teams:
            if player in blue:
                name = "🔵 " + name
            else:
                name = "🔴 " + name
        if player in tops:
            if player == tops[0]:
                name += " 🥇"
            elif player == tops[1]:
                name += " 🥈"
            else:
                name += " 🥉"
        embed.add_field(name=name, value=str(sortD[player])[:5], inline=False)
    embed.set_thumbnail(url="http://s.ppy.sh/a/" + top_id)
    await inter.edit_original_response(embed=embed)

bot.run(TOKEN)