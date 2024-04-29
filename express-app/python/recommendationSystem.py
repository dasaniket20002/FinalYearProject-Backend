import threading

'''
    UTILS_START
    Utility functions
'''
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


''''''
def getDefaultParams(access_token, max_results=10, region_code='IN', params_type=None):
    if params_type == 'videos':
        parts = ['snippet', 'contentDetails', 'id', 'topicDetails']
    elif params_type == 'search':
        parts = ['id', 'snippet']
    elif params_type == 'userinfo':
        return {'access_token': access_token}
    else:
        parts = ['id', 'snippet']

    params = {
        'type': 'video',
        'part' : ','.join(parts),
        'maxResults': max_results,
        'regionCode': region_code,
    }

    return params


''''''
def getDefaultHeaders(access_token, token_type):
    header = {
        'Authorization': f'{token_type} {access_token}'
    }
    return header


''''''
def prepare_params_for_search_request(access_token, order, max_results=10, region_code='IN', channel_id=None, search_query=None): # order : viewCount | date
    params = getDefaultParams(access_token, max_results, region_code, 'search')
    if(channel_id != None):
        params['channelId'] = channel_id
    if(search_query != None):
        params['q'] = search_query

    params['order'] = order
    return params

    # url_str = url.urlunparse(consts.YT_SEARCH_LINK, params=url.urlencode(params))
    # return url_str


''''''
def prepare_params_for_video_request(access_token, video_ids, max_results=10, region_code='IN'): 
    params = getDefaultParams(access_token, max_results, region_code, 'videos')
    params['id'] = ','.join(video_ids)
    return params

    # url_str = url.urlunparse(consts.YT_VIDEO_LINK, params=url.urlencode(params))
    # return url_str


''''''
def prepare_params_for_channel_request(access_token, channel_ids, max_results=10, region_code='IN'): 
    params = getDefaultParams(access_token, max_results, region_code)
    params['id'] = ','.join(channel_ids)
    return params

    # url_str = url.urlunparse(consts.YT_CHANNEL_LINK, params=url.urlencode(params))
    # return url_str

'''
    UTILS_END
'''


def get_recommendations(access_token, token_type, watched_tags, max_results, region_code):
    result = {}
    inp_data = {'access_token': access_token, 'token_type': token_type, 'watched_tags': watched_tags, 'max_results': max_results, 'region_code': region_code}

    # channel_thread = threading.Thread(name='channel_thread', target=get_recommendation_by_channel_ids, args=(watched_channel_ids, result, ))
    tags_thread = threading.Thread(name='tags_thread', target=get_recommendation_by_tags, args=(inp_data, result, ))
    # topics_thread = threading.Thread(name='topics_thread', target=get_recommendation_by_topics, args=(watched_topics, result, ))

    # channel_thread.start()
    tags_thread.start()
    # topics_thread.start()

    # channel_thread.join()
    tags_thread.join()
    # topics_thread.join()

    # try:
    #     print(str(result))
    # except:
    #     print('pass')

    video_list = []
    if(result['TAGS_RES'] != None):
        video_list = video_list + result['TAGS_RES']['video_list']

    return {
            'kind': 'api#recommendations',
            # 'videos_by_channel_id' : result['CHANNELS_RES'],
            'videos_by_top_tags' : result['TAGS_RES'],
            # 'videos_by_top_topics' : result['TOPICS_RES']
            'video_list': video_list
            }


import numpy as np
import pandas as pd
import grequests

from sklearn.feature_extraction.text import TfidfVectorizer

YT_SEARCH_LINK = 'https://youtube.googleapis.com/youtube/v3/search'
YT_VIDEOS_LINK = 'https://youtube.googleapis.com/youtube/v3/videos'
YT_CHANNEL_LINK = 'https://youtube.googleapis.com/youtube/v3/channels'

def get_recommendation_by_tags(inp_data, result_dict=None) :

    access_token = inp_data['access_token']
    token_type = inp_data['token_type']
    watched_tags = inp_data['watched_tags']
    max_results = inp_data['max_results']
    region_code = inp_data['region_code']

    if len(watched_tags) == 0 :
        if result_dict is not None:
            result_dict['TAGS_RES'] = None
        return None

    vectorizer = TfidfVectorizer(max_features=250, stop_words='english')

    vectorized_tags = vectorizer.fit_transform(watched_tags)
    vectorized_tags_DF = pd.DataFrame(vectorized_tags.toarray(), index=watched_tags, columns=vectorizer.get_feature_names_out())
    vectorized_tags_DF.loc[len(vectorized_tags_DF.index)] = abs(vectorized_tags_DF.sum() - 1)

    sorted_tags = (vectorized_tags_DF.iloc[-1].sort_values(ascending=False))
    reduced_sorted_tags = sorted_tags[0: 10 if len(sorted_tags) > 10 else len(sorted_tags)]

    default_header = getDefaultHeaders(access_token, token_type)

    params_for_videos_to_search_by_top_tags = [prepare_params_for_search_request(access_token, 'date' if np.random.rand() > 0.75 else 'viewCount', max_results, region_code, search_query=single_tag) for single_tag in reduced_sorted_tags.index]
    search_results = grequests.map(grequests.get(YT_SEARCH_LINK, params=params, headers=default_header) for params in params_for_videos_to_search_by_top_tags)

    # try:
    #     print([response.json() for response in search_results])
    # except:
    #     print('pass')

    if ['error'] in [list(response.json().keys()) for response in search_results]:
        if result_dict is not None:
            result_dict['TAGS_RES'] = None
        return None
    
    items_in_search_response = [x for xs in [response.json()['items'] for response in search_results] for x in xs]
    video_ids = [item['videoId'] for item in [item['id'] for item in items_in_search_response]]
    channel_ids = [item['channelId'] for item in [item['snippet'] for item in items_in_search_response]]

    video_search_results = grequests.map(
        [grequests.get(YT_VIDEOS_LINK, params=prepare_params_for_video_request(access_token, video_ids, max_results, region_code), headers=default_header),
        grequests.get(YT_CHANNEL_LINK, params=prepare_params_for_channel_request(access_token, channel_ids, max_results, region_code), headers=default_header)]
                )

    # try:
    #     print(video_search_results[0].json())
    # except:
    #     print('pass')
    # try:
    #     print(video_search_results[1].json())
    # except:
    #     print('pass')

    curated_video_list = clean_videos_list(video_search_results[0].json()['items'], video_search_results[1].json()['items'])

    return_obj = {
        'kind': 'TAGS_RES',
        'video_list': curated_video_list
    }

    if result_dict is not None:
        result_dict['TAGS_RES'] = return_obj
    return return_obj

'''
------------------------------------------------------------------------------------------------------------------------------------
'''

import sys
import json

args_path = sys.argv[1]
result_path = sys.argv[2]

json_str = open(args_path)
args = json.load(json_str)

access_token = args['access_token']
token_type = args['token_type']
watched_tags = args['watched_tags']
max_results = args['max_results']
region_code = args['region_code']


result = get_recommendations(access_token, token_type, watched_tags, max_results, region_code)
# print(str(result))

with open(result_path, "w") as outfile:
    json_object_result = json.dumps(result, indent=4)
    outfile.write(json_object_result)
print("OK")

sys.stdout.flush()