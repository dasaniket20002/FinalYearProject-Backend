from flask import request
from pymongo import MongoClient
from utils import consts

def update_user_data():

    CLIENT = MongoClient(f"mongodb+srv://{consts.MONGO_ID}:{consts.MONGO_PASS}@cluster0.xc9x9f1.mongodb.net/")
    DB = CLIENT[consts.MONGO_DB_NAME]

    data = request.get_json()
    sub = data.get('sub')
    channel_add = data.get('channel')
    tags_add = data.get('tags')
    topics_add = data.get('topics')

    user = DB.users.find_one({'sub': sub})

    if not user:
        return 'user doesnot exist', 400
    
    channels = user['channels']
    tags = user['tags']
    topics = user['topics']

    channels.insert(0, channel_add)
    for t in tags_add:
        tags.insert(0, t)
    for t in topics_add:
        topics.insert(0, t)

    channels = tags[:consts.WATCHED_TAGS_MAX_LENGTH if len(channels) > consts.WATCHED_TAGS_MAX_LENGTH else len(channels)]
    tags = tags[:consts.WATCHED_TAGS_MAX_LENGTH if len(tags) > consts.WATCHED_TAGS_MAX_LENGTH else len(tags)]
    topics = tags[:consts.WATCHED_TAGS_MAX_LENGTH if len(topics) > consts.WATCHED_TAGS_MAX_LENGTH else len(topics)]

    upd_filter = {'sub': sub}
    upd_content = {'$set': {'channels': channels, 'tags': tags, 'topics': topics}}

    DB.users.update_one(upd_filter, upd_content)
    return 'Updated user taste', 200

def get_user_tags_list(sub):
    CLIENT = MongoClient(f"mongodb+srv://{consts.MONGO_ID}:{consts.MONGO_PASS}@cluster0.xc9x9f1.mongodb.net/")
    DB = CLIENT[consts.MONGO_DB_NAME]
    print(CLIENT.list_databases())

    user = DB.users.find_one({'sub': sub})
    return user['tags']

def get_user_topics_list(sub):
    CLIENT = MongoClient(f"mongodb+srv://{consts.MONGO_ID}:{consts.MONGO_PASS}@cluster0.xc9x9f1.mongodb.net/")
    DB = CLIENT[consts.MONGO_DB_NAME]

    user = DB.users.find_one({'sub': sub})
    return user['topics']

def get_user_channels_list(sub):
    CLIENT = MongoClient(f"mongodb+srv://{consts.MONGO_ID}:{consts.MONGO_PASS}@cluster0.xc9x9f1.mongodb.net/")
    DB = CLIENT[consts.MONGO_DB_NAME]

    user = DB.users.find_one({'sub': sub})
    return user['channels']