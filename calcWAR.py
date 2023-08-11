from scipy import stats
import numpy as np
import requests
import util
from statistics import mean, median, stdev

# This wrapper function takes in a maps dict, api key, and api url,
# uses the map_war function to calculate WAR, and provides results 
# in the form of a dictionary with usernames as keys and
# normalized WAR as values.
def war_wrapper(maps, api_key, url):
    user_ids = {}
    for map in maps:
        map_war(map, user_ids)
    # swap to username
    results = {}
    for user in user_ids:
        username = util.user_from_id(api_key, user, url)
        results[username] = user_ids[user]
    warMean = abs(mean(results.values()))
    if warMean:
        for player in results:
            results[player] /= warMean
    return results

# This function takes in a map and results dict.
# This map calculates the WAR and adds the
# players' scores to the results dictionary.

def map_war(map, results):
    scores = map["scores"]
    

    # scoresArr = []
    # team1 = 0
    # team2 = 0
    # for score in scores:
    #     scoresArr.append(int(score["score"]))
    #     if score["team"] == '1':
    #         team1 += int(score["score"])
    #     else:
    #         team2 += int(score["score"])
    
    # cutoff = np.percentile(scoresArr, 25)

    # # alternative cutoff formats
    # # cutoff = mean(scoresArr) - stdev(scoresArr)
    # # cutoff = mean(scoresArr)
    # # cutoff = median(scoresArr)
    # if team1 > team2:
    #     winner = 1
    # else:
    #     winner = 2
    # diff = abs(team1 - team2)
    # for score in scores:
    #     if score["user_id"] not in results:
    #         results[score["user_id"]] = 0
    #     scoreComp = int(score["score"]) - cutoff
    #     if scoreComp > diff or (-1 * scoreComp) > diff:
    #         results[score["user_id"]] += scoreComp
    return results