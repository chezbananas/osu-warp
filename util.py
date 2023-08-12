# This file contains utility functions to be used
# by other functions.
import requests

# this function takes in a key, MP ID, and API URL
# it returns the maps dict from the game. (ignores the header info)
def getMaps(key, id, url):
    parameters = {
        "k": key,
        "mp": id
    }
    response = requests.get(url + "get_match", params=parameters)
    response = response.json()
    maps = response["games"]
    return maps

# This function takes in a key, MP ID, and API URL, and
# returns the match's name.
def getMatchName(key, id, url):
    parameters = {
        "k": key,
        "mp": id
    }
    response = requests.get(url + "get_match", params=parameters)
    response = response.json()
    result = response["match"]["name"]
    return result

# This helper function takes in a user ID and API key/url, and 
# returns their rank.
def get_rank(key, user, url):
    parameters = {
        "k": key,
        "u": user
    }
    response = requests.get(url + "user", params=parameters)
    response = response.json()
    if not response:
        return 0
    response = response[0]
    rank = response["pp_rank"]
    return rank

# This helper function takes in a user ID and API key/url, and 
# returns their username as a string.
def user_from_id(key, id, url):
    parameters = {
        "k": key,
        "u": id
    }
    response = requests.get(url + "get_user", params=parameters)
    response = response.json()
    if not response:
        return "Invalid User"
    response = response[0]
    username = response["username"]
    return username

# This helper function takes in a user ID and API key/url, and 
# returns their username as a string.
def id_from_user(key, username, url):
    parameters = {
        "k": key,
        "u": username
    }
    response = requests.get(url + "get_user", params=parameters)
    response = response.json()
    if not response:
        return "Invalid User"
    response = response[0]
    id = response["user_id"]
    return id