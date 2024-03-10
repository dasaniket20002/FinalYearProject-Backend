from recommendationSystem import recommendByChannelID as ch
from recommendationSystem import recommendByTags as tgs
from recommendationSystem import recommendByTopics as tps

def get_recommendations(youtube, watched_channel_ids, watched_topics, watched_tags, language_spoken='en', country_code='IN'):
    videos_by_channel_id = ch.get_recommendation_by_channel_id(youtube, watched_channel_ids, language_spoken, country_code)
    videos_by_top_tags = tgs.get_recommendation_by_tags(youtube, watched_tags, language_spoken, country_code)
    videos_by_top_topics = tps.get_recommendation_by_topics(youtube, watched_topics, language_spoken, country_code)

    videos = []
    if videos_by_channel_id is not None :
        videos = videos + videos_by_channel_id
    if videos_by_top_tags is not None :
        videos = videos + videos_by_top_tags
    if videos_by_top_topics is not None :
        videos = videos + videos_by_top_topics

    return {'videos' : videos,
            'videos_by_channel_id' : videos_by_channel_id,
            'videos_by_top_tags' : videos_by_top_tags,
            'videos_by_top_topics' : videos_by_top_topics
            }