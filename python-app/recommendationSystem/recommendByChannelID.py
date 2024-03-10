import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import searchFunctions.searchByChannelID as sr
from utils import utils

def get_recommendation_by_channel_id(youtube, watched_channel_ids, language_spoken, country_code) :
    if len(watched_channel_ids) == 0 :
        return None

    vectorizer = CountVectorizer(max_features=250, stop_words='english')

    vectorized_channels = vectorizer.fit_transform(watched_channel_ids)
    vectorized_channels_DF = pd.DataFrame(vectorized_channels.toarray(), index=watched_channel_ids, columns=vectorizer.get_feature_names_out())
    vectorized_channels_DF.loc[len(vectorized_channels_DF.index)] = abs(vectorized_channels_DF.sum() - 1)

    sorted_channels = (vectorized_channels_DF.iloc[-1].sort_values(ascending=False))
    reduced_sorted_channels = sorted_channels[0: 5 if len(sorted_channels) > 5 else len(sorted_channels)]

    videos_by_channel_id = []
    for watched_channel_id in reduced_sorted_channels.index :
        videos_to_add = sr.get_most_recent_videos_by_channel_id(youtube, watched_channel_id, language_spoken, country_code) if np.random.rand() > 0.5 else sr.get_most_popular_videos_by_channel_id(youtube, watched_channel_id, language_spoken, country_code)
        videos_by_channel_id = videos_by_channel_id + videos_to_add
    return utils.filter_shorts(videos_by_channel_id)