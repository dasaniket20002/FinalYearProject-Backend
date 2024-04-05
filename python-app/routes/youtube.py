from youtubeFunctions import search, trending, recommendation_system
from cachetools import TTLCache


cache = TTLCache(maxsize=1000, ttl=600)

# GET TRENDING VIDEOS LIST

def getTrending():
    return trending.getTrending(cache)
def getPagedTrending():
    return trending.getPage(cache)


# GET SEARCHED VIDEOS LIST

def getSearch():
    return search.getSearch(cache)
def getPagedSearch():
    return search.getPage(cache)


def getAllRecommendations():
    return recommendation_system.get_recommendations()


def getRecommendationsByTags():
    return {}


def getRecommendationByTopics():
    return {}


def getRecommedationByChannels():
    return {}