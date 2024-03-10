from dotenv import load_dotenv
import os

load_dotenv()

SEARCH_LIST_API_CALL_COUNT = 0
VIDEO_LIST_API_CALL_COUNT = 0

CHANNEL_SEARCH_CALL_COUNT = 0
TOPIC_SEARCH_CALL_COUNT = 0

YT_API_KEY = os.getenv('YT_API_KEY')
API_VERSION = os.getenv('API_VERSION')
API_NAME = os.getenv('API_NAME')

MAX_YT_SEARCH_RESULTS = os.getenv('MAX_YT_SEARCH_RESULTS')