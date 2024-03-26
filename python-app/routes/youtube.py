from youtubeFunctions import search, trending
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



def getRecommendationsByTags():
    return {}


def getRecommendationByTopics():
    return {}


def getRecommedationByChannels():
    return {}