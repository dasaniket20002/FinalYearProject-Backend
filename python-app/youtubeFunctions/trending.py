from urllib import parse as url

from flask import request
from utils import consts, utilities
import requests

def getContent(cache, params, headers):
    link_to_get = consts.YT_VIDEO_LINK + '?' + url.urlencode(params)
    if link_to_get in cache:
        return cache[link_to_get]

    response = requests.get(consts.YT_VIDEO_LINK, params=params, headers=headers)
    responseObj = response.json()
    
    if response.status_code != 200:
        return { 'err': responseObj['error'] }
    
    cleaned_video_list = utilities.clean_videos_list(responseObj['items'])
    returnObj = {
        'video_list' : cleaned_video_list
    }
    if 'kind' in responseObj.keys():
        returnObj['kind'] = responseObj['kind']
    if 'nextPageToken' in responseObj.keys():
        returnObj['nextPageToken'] = responseObj['nextPageToken']
    if 'prevPageToken' in responseObj.keys():
        returnObj['prevPageToken'] = responseObj['prevPageToken']
    cache[link_to_get] = returnObj

    return returnObj

def getTrending(cache):
    params = utilities.getDefaultParams('videos')
    params['chart'] = 'mostPopular'

    headers = utilities.getDefaultHeaders()

    return getContent(cache, params, headers)

def getPage(cache):
    params = utilities.getDefaultParams('videos')
    params['chart'] = 'mostPopular'
    params['pageToken'] = request.args.get('page_token')

    return getContent(cache, params)