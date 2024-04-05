import threading

from flask import request
from youtubeFunctions import recommendations_by_tags


def get_recommendations():

    sub = request.args.get('sub')

    result = {}

    # channel_thread = threading.Thread(name='channel_thread', target=get_recommendation_by_channel_ids, args=(watched_channel_ids, result, ))
    tags_thread = threading.Thread(name='tags_thread', target=recommendations_by_tags.get_recommendation_by_tags, args=(sub, result, ))
    # topics_thread = threading.Thread(name='topics_thread', target=get_recommendation_by_topics, args=(watched_topics, result, ))

    # channel_thread.start()
    tags_thread.start()
    # topics_thread.start()

    # channel_thread.join()
    tags_thread.join()
    # topics_thread.join()

    print(result)

    return {
            # 'videos_by_channel_id' : result['CHANNELS_RES'],
            'videos_by_top_tags' : result['TAGS_RES'],
            # 'videos_by_top_topics' : result['TOPICS_RES']
            }