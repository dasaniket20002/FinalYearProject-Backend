import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import searchFunctions.searchByTopic as sr
from utils import utils

def get_recommendation_by_tags(youtube, watched_tags, language_spoken, country_code) :
    if len(watched_tags) == 0 :
        return None

    vectorizer = TfidfVectorizer(max_features=250, stop_words='english')

    vectorized_tags = vectorizer.fit_transform(watched_tags)
    vectorized_tags_DF = pd.DataFrame(vectorized_tags.toarray(), index=watched_tags, columns=vectorizer.get_feature_names_out())
    vectorized_tags_DF.loc[len(vectorized_tags_DF.index)] = abs(vectorized_tags_DF.sum() - 1)

    sorted_tags = (vectorized_tags_DF.iloc[-1].sort_values(ascending=False))
    reduced_sorted_tags = sorted_tags[0: 10 if len(sorted_tags) > 10 else len(sorted_tags)]

    videos_by_top_tags = []
    for single_tag in reduced_sorted_tags.index :
        videos_to_add = sr.get_most_recent_videos_by_topic(youtube, single_tag, language_spoken, country_code) if np.random.rand() > 0.5 else sr.get_most_popular_videos_by_topic(youtube, single_tag, language_spoken, country_code)
        videos_by_top_tags = videos_by_top_tags + videos_to_add

    return utils.filter_shorts(videos_by_top_tags)