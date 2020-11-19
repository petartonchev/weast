import pickle
import numpy as np
from preprocessing import sentiment_analysis_pipeline, filtering_pipeline
from preprocessing import convert_array


with open('sentiment_analysis.sav', 'rb') as model_file:
    sentiment_model = pickle.load(model_file)


def get_embeddings(words):
    from app import mongo

    embedded_words = []
    word_embeddings = mongo.db.glove.find({'word': {"$in": words}})
    for word in word_embeddings:
        embedded_words.append(convert_array(word['embedding']))

    return embedded_words


def vecs_to_sentiment(vecs):
    predictions = sentiment_model.predict_log_proba(vecs)
    # Free the memory as it doesn't get deleted automatically when deployed to heroku
    del vecs
    return predictions[:, 1] - predictions[:, 0]


def words_to_sentiment(words):
    vecs = get_embeddings(words)
    return vecs_to_sentiment(vecs)


def text_to_sentiment(tokens):
    sentiments = words_to_sentiment(tokens)
    pos = sum([1 for s in sentiments if s >= 0])
    neg = sum([1 for s in sentiments if s < 0])

    if pos >= neg:
        return 1
    else:
        return -1


def predict_sentiment(tweet, tweet_preprocessed=False):
    if not tweet_preprocessed:
        tweet = filtering_pipeline(tweet)

    tweet = sentiment_analysis_pipeline(tweet)
    if len(tweet) > 0:
        return text_to_sentiment(tweet)
    else:
        return None
