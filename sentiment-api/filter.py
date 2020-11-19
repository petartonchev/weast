import numpy as np
import json
# Deep Learning
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import tensorflow as tf

from preprocessing import filtering_pipeline

MAX_SEQUENCE_LENGTH = 300


def tokenizer_from_json(json_string):
    """Parses a JSON tokenizer configuration file and returns a
    tokenizer instance.
    # Arguments
        json_string: JSON string encoding a tokenizer configuration.
    # Returns
        A Keras Tokenizer instance
    """
    tokenizer_config = json.loads(json_string)
    config = tokenizer_config.get('config')

    word_counts = json.loads(config.pop('word_counts'))
    word_docs = json.loads(config.pop('word_docs'))
    index_docs = json.loads(config.pop('index_docs'))
    # Integer indexing gets converted to strings with json.dumps()
    index_docs = {int(k): v for k, v in index_docs.items()}
    index_word = json.loads(config.pop('index_word'))
    index_word = {int(k): v for k, v in index_word.items()}
    word_index = json.loads(config.pop('word_index'))

    tokenizer = Tokenizer(**config)
    tokenizer.word_counts = word_counts
    tokenizer.word_docs = word_docs
    tokenizer.index_docs = index_docs
    tokenizer.word_index = word_index
    tokenizer.index_word = index_word

    return tokenizer


with open('tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)

global filter_model, graph
# initialize these variables
filter_model = load_model('tweet-filter-50-lstm-cpu.h5')
graph = tf.get_default_graph()


def classify_tweet_relevance(tweet_text):
    processed_tweet = filtering_pipeline(tweet_text)
    if len(processed_tweet) == 0:
        return False, processed_tweet

    # Extract features
    x_tweet_features = np.array(tokenizer.texts_to_sequences(processed_tweet))
    x_tweet_features = pad_sequences(x_tweet_features, maxlen=MAX_SEQUENCE_LENGTH)

    with graph.as_default():
        y_predict_tweets = [1 if o > 0.5 else 0 for o in filter_model.predict(x_tweet_features)]

    # invert the label since 0 means good, 1 means bad
    is_relevant = not bool( y_predict_tweets[0])
    return is_relevant, processed_tweet
