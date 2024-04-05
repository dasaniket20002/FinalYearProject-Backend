from flask import request
from utils import consts

def signin():
    data = request.get_json()
    sub = data.get('sub')

    if not consts.DB.users.find_one({'sub': sub}):
        consts.DB.users.insert_one({'sub': sub, 'channels': [], 'tags': [], 'topics': []})
        return "User Added!", 200

    return "User Exists!", 201
    