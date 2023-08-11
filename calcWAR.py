from scipy import stats
from numpy.random import normal
import util
from statistics import mean, median, stdev

NUM_TRIALS = 5000

# This wrapper function takes in a maps dict, api key, and api url,
# Uses the map_war function to calculate WAR, and provides results 
# in the form of a dictionary with usernames as keys and
# normalized WAR as values.
def war_wrapper(maps, api_key, url):
    user_ids = {}
    playcount = {}
    blue = set()  # keep track of teams
    for map in maps:
        map_war(map, user_ids, playcount, blue)
    mPC = median([playcount[user] for user in playcount])
    # swap to username
    results = {}
    blueNames = set()
    for user in user_ids:
        username = util.user_from_id(api_key, user, url)
        results[username] = user_ids[user] * (playcount[user] / mPC) ** (1 / 3) / playcount[user]
        if user in blue:
            blueNames.add(username)
    factor = 1 / mean(results.values())
    normalised_results = {user: cost * factor for user, cost in results.items() }
    return normalised_results, blueNames

# This function takes in a map and results dict.
# This map calculates the WAR using a monte carlo
# simulation and adds the players' scores to the
# results and playcount dictionary.
def map_war(map, results, playcount, blue):
    scores = map["scores"]
    scoresArr = []
    for score in scores:
        scoresArr.append(int(score["score"]))
    sm = mean(scoresArr)
    std = stdev(scoresArr)
    for score in scores:
        w = 0
        for i in range(NUM_TRIALS):
            samples = normal(sm, std, 7)
            t1 = sum(samples[:4])
            t2 = sum(samples[4:])
            if int(score["score"]) + t2 > t1:
                w += 1
        w /= NUM_TRIALS
        id = score["user_id"]
        if id not in results:
            results[id] = 0
            playcount[id] = 0
        results[id] += w
        playcount[id] += 1
        if score["team"] == '1':
            blue.add(score[id])