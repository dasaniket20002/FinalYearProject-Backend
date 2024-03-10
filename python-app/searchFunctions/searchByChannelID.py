from utils import consts

def get_most_recent_videos_by_channel_id(youtube, channel_id, language_spoken, country_code, max_results=consts.MAX_YT_SEARCH_RESULTS):

    # Call the search.list method to search for videos from the specified channel
    consts.SEARCH_LIST_API_CALL_COUNT += 1
    search_response = youtube.search().list(
        channelId=channel_id,
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
    for video in video_details.get('items', []):
        video = {
            'title': video['snippet']['title'],
            'video_id': video['id'],
            'topic_details': [s[30:] for s in video['topicDetails']['topicCategories']],
            'video_tags': video['snippet']['tags'] if 'tags' in video['snippet'].keys() else None
        }
        videos.append(video)

    consts.CHANNEL_SEARCH_CALL_COUNT += 1
    return videos

def get_most_popular_videos_by_channel_id(youtube, channel_id, language_spoken, country_code, max_results=consts.MAX_YT_SEARCH_RESULTS):

    # Call the search.list method to search for videos from the specified channel
    consts.SEARCH_LIST_API_CALL_COUNT += 1
    search_response = youtube.search().list(
        channelId=channel_id,
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
        video = {
            'title': video['snippet']['title'],
            'video_id': video['id'],
            'topic_details': [s[30:] for s in video['topicDetails']['topicCategories']],
            'video_tags': video['snippet']['tags'] if 'tags' in video['snippet'].keys() else None
        }
        videos.append(video)

    consts.CHANNEL_SEARCH_CALL_COUNT += 1
    return videos