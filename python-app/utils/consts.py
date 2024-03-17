import os
from dotenv import load_dotenv
load_dotenv()

MAX_YT_SEARCH_RESULTS = 20
BATCH_MAX_YT_SEARCH_RESULTS = 5

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
API_KEY = os.getenv('API_KEY')
PORT = os.getenv('PORT')

API_NAME = 'youtube'
API_VERSION = 'v3'
API_BASE_URL = f'https://youtube.googleapis.com/{API_NAME}/{API_VERSION}'

VIDEOS_RULE = 'videos'
SEARCH_RULE = 'search'

YT_VIDEO_LINK = f'{API_BASE_URL}/{VIDEOS_RULE}'
YT_SEARCH_LINK = f'{API_BASE_URL}/{SEARCH_RULE}'