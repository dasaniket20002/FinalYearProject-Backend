from flask import request
from urllib import parse as url
from utils import consts, utilities
import requests


def getContent(cache, params, headers):
    link_to_get = consts.YT_SEARCH_LINK + '?' + url.urlencode(params)
    if link_to_get in cache:
        return cache[link_to_get]
    
    response = requests.get(consts.YT_SEARCH_LINK, params=params, headers=headers)
    searchResponseObj = response.json()
        
    if response.status_code != 200:
        return { 'err': searchResponseObj['error'] }
    
    params = utilities.getDefaultParams('videos')
    params['id'] = ','.join([video['id']['videoId'] for video in searchResponseObj['items'] if video['id']['kind'] == 'youtube#video'])

    response = requests.get(consts.YT_VIDEO_LINK, params=params, headers=headers)
    videosResponseObj = response.json()

    if response.status_code != 200:
            return { 'err': videosResponseObj['error'] }
    
    params = utilities.getDefaultParams()
    params['id'] = ','.join([video['snippet']['channelId'] for video in searchResponseObj['items'] if video['id']['kind'] == 'youtube#video'])
    
    response = requests.get(consts.YT_CHANNEL_LINK, params=params, headers=headers)
    channelsResponseObj = response.json()

    cleaned_video_list = utilities.clean_videos_list(videosResponseObj['items'], channelsResponseObj['items'])
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

    headers = utilities.getDefaultHeaders()

    return getContent(cache, params, headers)

def getPage(cache):
    params = utilities.getDefaultParams('search')
    params['pageToken'] = request.args.get('page_token')

    headers = utilities.getDefaultHeaders()

    return getContent(cache, params, headers)