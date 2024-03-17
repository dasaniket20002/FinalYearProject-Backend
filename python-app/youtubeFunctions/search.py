from flask import request
from urllib import parse as url
from utils import consts, utilities
import requests


def getContent(cache, params):
    link_to_get = consts.YT_SEARCH_LINK + '?' + url.urlencode(params)
    if link_to_get in cache:
        searchResponseObj = cache[link_to_get]
    else:
        response = requests.get(link_to_get)
        searchResponseObj = response.json()
        
        if response.status_code != 200:
            return { 'err': searchResponseObj['error'] }
        
        cache[link_to_get] = searchResponseObj
    
    params = utilities.getDefaultParams('videos')
    params['id'] = ','.join([video['id']['videoId'] for video in searchResponseObj['items']])

    link_to_get = consts.YT_VIDEO_LINK + '?' + url.urlencode(params)
    if link_to_get in cache:
        return cache[link_to_get]

    response = requests.get(link_to_get)
    videosResponseObj = response.json()

    if response.status_code != 200:
            return { 'err': videosResponseObj['error'] }

    cleaned_video_list = utilities.clean_videos_list(videosResponseObj['items'])
    returnObj = {
        'video_list' : cleaned_video_list
    }
    if 'kind' in searchResponseObj.keys():
        returnObj['kind'] = searchResponseObj['kind']
    if 'nextPageToken' in searchResponseObj.keys():
        returnObj['nextPageToken'] = searchResponseObj['nextPageToken']
    if 'prevPageToken' in searchResponseObj.keys():
        returnObj['prevPageToken'] = searchResponseObj['prevPageToken']
    cache[link_to_get] = returnObj

    return returnObj 


def getSearch(cache):
    params = utilities.getDefaultParams('search')
    params['q'] = request.args.get('q')

    return getContent(cache, params)

def getPage(cache):
    params = utilities.getDefaultParams('search')
    params['pageToken'] = request.args.get('page_token')

    return getContent(cache, params)