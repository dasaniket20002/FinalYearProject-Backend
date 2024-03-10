import requests
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


def is_not_shorts_video(video):
    url = 'https://www.youtube.com/shorts/' + video['video_id']
    ret = requests.head(url)
    # whether 303 or other values, it's not short
    return ret.status_code != 200

def filter_shorts(videos):
    return [v for v in videos if is_not_shorts_video(v)]



def stem_tags(videos):
    ps = PorterStemmer()
    for video in videos:
        if 'video_tags' in video.keys() and video['video_tags'] is not None:
            video['video_tags'] = [ps.stem(tag) for tag in video['video_tags']]
    return videos



def remove_stopword_tags(videos):
    stop_words = set(stopwords.words('english'))
    for video in videos:
        if 'video_tags' in video.keys() and video['video_tags'] is not None:
            video['video_tags'] = list(filter(lambda x:x not in stop_words, video['video_tags']))
    return videos