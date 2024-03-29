from flask import request
from urllib import parse as url

from utils import consts


def construct_clean_structure(video, channel):
    return_dict = {}

    videos_keys = video.keys()
    if 'kind' in videos_keys :
        return_dict['kind'] = video['kind']

    if 'id' in videos_keys :
        return_dict['id'] = video['id']
    
    if 'snippet' in videos_keys:
        snippet_keys = video['snippet'].keys()

        if 'description' in snippet_keys:
            return_dict['description'] = video['snippet']['description']

        if 'publishedAt' in snippet_keys:
            return_dict['publishedAt'] = video['snippet']['publishedAt']

        if 'title' in snippet_keys :
            return_dict['title'] = video['snippet']['title']

        if 'channelId' in snippet_keys :
            return_dict['channelId'] = video['snippet']['channelId']
        if 'channelTitle' in snippet_keys :
            return_dict['channelTitle'] = video['snippet']['channelTitle']

        if 'thumbnails' in snippet_keys :
            if 'high' in video['snippet']['thumbnails'].keys() :
                return_dict['thumbnail'] = video['snippet']['thumbnails']['high']
        if 'defaultLanguage' in snippet_keys :
            return_dict['defaultLanguage'] = video['snippet']['defaultLanguage']
        if 'defaultAudioLanguage' in snippet_keys :
            return_dict['defaultAudioLanguage'] = video['snippet']['defaultAudioLanguage']

        if 'tags' in snippet_keys :
            return_dict['tags'] = video['snippet']['tags']

    if 'contentDetails' in videos_keys:
        content_details_keys = video['contentDetails'].keys()

        if 'duration' in content_details_keys :
            return_dict['duration'] = video['contentDetails']['duration']
        if 'definition' in content_details_keys :
            return_dict['definition'] = video['contentDetails']['definition']
    
    if 'topicDetails' in videos_keys :
        return_dict['topicDetails'] = [s[30:] for s in video['topicDetails']['topicCategories']]

    if 'pageInfo' in videos_keys:
        return_dict['pageInfo'] = video['pageInfo']

    if 'snippet' in channel.keys():
        if 'thumbnails' in channel['snippet'].keys():
            return_dict['channelThumbnail'] = channel['snippet']['thumbnails']['default']

    return return_dict

def clean_videos_list(video_list, channel_list):
    video_channel_list = [(video, channel) for video in video_list for channel in channel_list if video['snippet']['channelId'] == channel['id']]
    return [construct_clean_structure(video, channel) for (video, channel) in video_channel_list]

def getDefaultParams(params_type=None):
    if params_type == 'videos':
        parts = ['snippet', 'contentDetails', 'id', 'topicDetails']
    elif params_type == 'search':
        parts = ['id', 'snippet']
    elif params_type == 'userinfo':
        return {'access_token': request.args.get('access_token')}
    else:
        parts = ['id', 'snippet']

    params = {
        'part' : ','.join(parts),
        'maxResults': consts.MAX_YT_SEARCH_RESULTS
    }

    region_code = request.args.get('region_code')

    if region_code is None:
        params['regionCode'] = 'IN'
    else:
        params['regionCode'] = region_code

    access_token = request.args.get('access_token')
    if not access_token: 
        params['key'] = consts.API_KEY

    return params

def getDefaultHeaders():
    access_token = request.args.get('access_token')
    token_type = request.args.get('token_type')

    header = {
        'Authorization': f'{token_type} {access_token}'
    }
    return header