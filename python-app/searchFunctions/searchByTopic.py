from utils import consts

def get_most_recent_videos_by_topic(youtube, topic, language_spoken, country_code, max_results=consts.MAX_YT_SEARCH_RESULTS):

    # Call the search.list method to search for videos on the specified topic
    consts.SEARCH_LIST_API_CALL_COUNT += 1
    search_response = youtube.search().list(
        q=topic,
        type='video',
        part='id',
        maxResults=max_results,
        order='date',  # Sort by date (most recent)
        relevanceLanguage=language_spoken,
        regionCode=country_code
    ).execute()

    video_ids = [result['id']['videoId'] for result in search_response.get('items', [])]

    # Call the videos.list method to retrieve video details
    consts.VIDEO_LIST_API_CALL_COUNT += 1
    video_details = youtube.videos().list(
        part='snippet, topicDetails',
        id=','.join(video_ids)
    ).execute()

    videos = []
    for video in video_details['items']:
        dict_to_append = {
            'title': video['snippet']['title'],
            'video_id': video['id']
        }
        if 'topicDetails' in video.keys() :
            dict_to_append['topic_details'] = [s[30:] for s in video['topicDetails']['topicCategories']]
        if 'tags' in video['snippet'].keys() :
            dict_to_append['video_tags'] = video['snippet']['tags']

        videos.append(dict_to_append)

    consts.TOPIC_SEARCH_CALL_COUNT += 1
    return videos

def get_most_popular_videos_by_topic(youtube, topic, language_spoken, country_code, max_results=consts.MAX_YT_SEARCH_RESULTS):

    # Call the search.list method to search for videos on the specified topic
    consts.SEARCH_LIST_API_CALL_COUNT += 1
    search_response = youtube.search().list(
        q=topic,
        type='video',
        part='id',
        maxResults=max_results,
        order='viewCount',  # Sort by viewCount (most viewed)
        relevanceLanguage=language_spoken,
        regionCode=country_code
    ).execute()

    video_ids = [result['id']['videoId'] for result in search_response.get('items', [])]

    # Call the videos.list method to retrieve video details
    consts.VIDEO_LIST_API_CALL_COUNT += 1
    video_details = youtube.videos().list(
        part='snippet, topicDetails',
        id=','.join(video_ids)
    ).execute()

    videos = []
    for video in video_details.get('items', []):
        dict_to_append = {
            'title': video['snippet']['title'],
            'video_id': video['id']
        }
        if 'topicDetails' in video.keys() :
            dict_to_append['topic_details'] = [s[30:] for s in video['topicDetails']['topicCategories']]
        if 'tags' in video['snippet'].keys() :
            dict_to_append['video_tags'] = video['snippet']['tags']

        videos.append(dict_to_append)

    consts.TOPIC_SEARCH_CALL_COUNT += 1
    return videos

