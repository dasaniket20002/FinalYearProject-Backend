from utils import consts

def search_youtube(youtube, query, language_spoken, country_code, max_results=consts.MAX_YT_SEARCH_RESULTS):

    # Call the search.list method to search for videos
    consts.SEARCH_LIST_API_CALL_COUNT += 1
    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=max_results,
        relevanceLanguage=language_spoken,
        regionCode=country_code
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video = {
                'title': search_result['snippet']['title'],
                'video_id': search_result['id']['videoId']
            }
            videos.append(video)

    return videos