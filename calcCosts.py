# This file contains functions that calculates RWS for osu matches.
# This is essentially the % of the score you provided for maps
# your team won, while giving 0% for maps you lost or didn't play.
# A little too results-oriented to provide meaningful results.
import util
from statistics import mean

def parseMaps(maps):
    result = {}
    for map in maps:
        map_id = map["beatmap_id"]
        scores = []
        for score in map["scores"]:
            d = {}
            d["team"] = score["team"]
            d["user"] = score["user_id"]
            d["score"] = score["score"]
            d["mods"] = score["enabled_mods"]
            scores.append(d)
        result[map_id] = scores
    print(len(result))
    return result

def costsWrapper(key, map, url):
    costs = calcCosts(map)
    result = {}
    for score in map:
        user = util.user_from_id(key, score["user"], url + "get_user")
        cost = costs[score["user"]]
        result[user] = cost
    return result

def calcCosts(map):
    team1 = []
    team2 = []
    team_size = 0
    for score in map:
        if score["team"] == '1':
            team1.append(int(score["score"]))
        else:
            team2.append(int(score["score"]))
        team_size += 1
    team_size /= 2
    sum1 = sum(team1)
    sum2 = sum(team2)
    if sum1 > sum2:
        winner = '1'
        winnerSum = sum1
    elif sum2 > sum1:
        winner = '2'
        winnerSum = sum2
    else:
        winner = '-1'  # tied, no one gets points
        winnerSum = 0
    costs = {}
    for score in map:
        if score["team"] == winner:
            costs[score["user"]] = int(score["score"]) / winnerSum * team_size
        else:
            costs[score["user"]] = 0
    return costs