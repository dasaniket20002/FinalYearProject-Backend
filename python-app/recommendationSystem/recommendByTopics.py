import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import searchFunctions.searchByTopic as sr
from utils import utils

def get_recommendation_by_topics(youtube, watched_topics, language_spoken, country_code) :
    if len(watched_topics) == 0 :
        return None

    vectorizer = TfidfVectorizer(max_features=250, stop_words='english')

    vectorized_topics = vectorizer.fit_transform(watched_topics)
    vectorized_topics_DF = pd.DataFrame(vectorized_topics.toarray(), index=watched_topics, columns=vectorizer.get_feature_names_out())
    vectorized_topics_DF.loc[len(vectorized_topics_DF.index)] = abs(vectorized_topics_DF.sum() - 1)

    sorted_topics = (vectorized_topics_DF.iloc[-1].sort_values(ascending=False))
    reduced_sorted_topics = sorted_topics[0: 5 if len(sorted_topics) > 5 else len(sorted_topics)]

    videos_by_top_topics = []
    for single_topic in reduced_sorted_topics.index :
        videos_to_add = sr.get_most_recent_videos_by_topic(youtube, single_topic, language_spoken, country_code) if np.random.rand() > 0.5 else sr.get_most_popular_videos_by_topic(youtube, single_topic, language_spoken, country_code)
        videos_by_top_topics = videos_by_top_topics + videos_to_add

    return utils.filter_shorts(videos_by_top_topics)