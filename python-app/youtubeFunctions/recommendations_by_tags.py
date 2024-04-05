import numpy as np
import pandas as pd
import grequests

from sklearn.feature_extraction.text import TfidfVectorizer

from utils import utilities, consts
from routes import db_ops

def get_recommendation_by_tags(sub, result_dict=None) :

    watched_tags = db_ops.get_user_tags_list(sub)

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

    default_header = utilities.getDefaultHeaders()

    params_for_videos_to_search_by_top_tags = [utilities.prepare_params_for_search_request('date' if np.random.rand() > consts.PROBABILITY_TO_SELECT_BY_VIEWCOUNT else 'viewCount', search_query=single_tag) for single_tag in reduced_sorted_tags.index]
    search_results = grequests.map(grequests.get(consts.YT_SEARCH_LINK, params=params, headers=default_header) for params in params_for_videos_to_search_by_top_tags)

    if ['error'] in [list(response.json().keys()) for response in search_results]:
        if result_dict is not None:
            result_dict['TAGS_RES'] = None
        return None
    
    next_page_token_list = [response.json()['nextPageToken'] for response in search_results]

    items_in_search_response = [x for xs in [response.json()['items'] for response in search_results] for x in xs]
    video_ids = [item['videoId'] for item in [item['id'] for item in items_in_search_response]]

    video_search_results = grequests.map(
        grequests.get(consts.YT_VIDEO_LINK, params=utilities.prepare_params_for_video_request(video_ids), headers=default_header),
        grequests.get(consts.YT_CHANNEL_LINK, params=utilities.prepare_params_for_channel_request(video_ids), headers=default_header)
                )

    # videos_results = requests.get(consts.YT_VIDEO_LINK, params=utilities.prepare_params_for_video_request(video_ids), headers=default_header).json()
    # channels_results = requests.get(consts.YT_CHANNEL_LINK, params=utilities.prepare_params_for_channel_request(video_ids), headers=default_header).json()

    curated_video_list = utilities.construct_clean_structure(video_search_results[0].json()['items'], video_search_results[1].json()['items'])

    return_obj = {
        'kind': 'TAGS_RES',
        'next_page_tokens': next_page_token_list,
        'video_list': curated_video_list
    }

    if result_dict is not None:
        result_dict['TAGS_RES'] = return_obj
    return return_obj

def get_recommendation_by_tags_page(next_page_tokens, result_dict=None) :
    default_header = utilities.getDefaultHeaders()

    params_for_videos_to_search_by_top_tags = []
    for next_page_token in next_page_tokens:
        param = utilities.getDefaultParams()
        param['pageToken'] = next_page_token
        params_for_videos_to_search_by_top_tags.append(param)
        
    search_results = grequests.map(grequests.get(consts.YT_SEARCH_LINK, params=params, headers=default_header) for params in params_for_videos_to_search_by_top_tags)

    if ['error'] in [list(response.json().keys()) for response in search_results]:
        if result_dict is not None:
            result_dict['TAGS_RES'] = None
        return None
    
    next_page_token_list = [response.json()['nextPageToken'] for response in search_results]

    items_in_search_response = [x for xs in [response.json()['items'] for response in search_results] for x in xs]
    video_ids = [item['videoId'] for item in [item['id'] for item in items_in_search_response]]

    video_search_results = grequests.map(
        grequests.get(consts.YT_VIDEO_LINK, params=utilities.prepare_params_for_video_request(video_ids), headers=default_header),
        grequests.get(consts.YT_CHANNEL_LINK, params=utilities.prepare_params_for_channel_request(video_ids), headers=default_header)
                )

    curated_video_list = utilities.construct_clean_structure(video_search_results[0].json()['items'], video_search_results[1].json()['items'])

    return_obj = {
        'kind': 'TAGS_RES',
        'next_page_tokens': next_page_token_list,
        'video_list': curated_video_list
    }

    if result_dict is not None:
        result_dict['TAGS_RES'] = return_obj
    return return_obj