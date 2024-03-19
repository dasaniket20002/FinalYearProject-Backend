from urllib import parse as url

from flask import request
from utils import consts, utilities
import requests

def getContent(cache, params, headers):
    link_to_get = consts.YT_VIDEO_LINK + '?' + url.urlencode(params)
    if link_to_get in cache:
        return cache[link_to_get]

    response = requests.get(consts.YT_VIDEO_LINK, params=params, headers=headers)
    responseObjVid = response.json()
    
    if response.status_code != 200:
        return { 'err': responseObjVid['error'] }
    
    channel_ids = ','.join([item['snippet']['channelId'] for item in responseObjVid['items']])
    params = utilities.getDefaultParams()
    params['id'] = channel_ids
    response = requests.get(consts.YT_CHANNEL_LINK, params=params, headers=headers)
    responseObjChnl = response.json()

    if response.status_code != 200:
        return { 'err': responseObjChnl['error'] }
    
    cleaned_video_list = utilities.clean_videos_list(responseObjVid['items'], responseObjChnl['items'])
    returnObj = {
        'video_list' : cleaned_video_list
    }
    if 'kind' in responseObjVid.keys():
        returnObj['kind'] = responseObjVid['kind']
    if 'nextPageToken' in responseObjVid.keys():
        returnObj['nextPageToken'] = responseObjVid['nextPageToken']
    if 'prevPageToken' in responseObjVid.keys():
        returnObj['prevPageToken'] = responseObjVid['prevPageToken']

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

    headers = utilities.getDefaultHeaders()

    return getContent(cache, params, headers)