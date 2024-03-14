from flask import request
from urllib import parse as url
from utils import consts
import os


def hello():
    return {'msg':'helloworld'}

def getTrending():
    API_KEY = os.getenv('')
    params = {
        'part' : ','.join(['snippet', 'contentDetails', 'id']),
        'chart': 'mostPopular',
        'maxResults': consts.MAX_YT_SEARCH_RESULTS,
        'regionCode': request.args.get('region_code'),
        'accessToken': request.args.get('access_token')
    }
    access_token = None | request.args.get('access_token')
    if(access_token != None):
        params['accessToken'] = request.args.get('access_token')
        params['key'] = os.getenv('API_KEY')

    link = consts.YT_VIDEO_LINK + '?' + url.urlencode(params)
    return link