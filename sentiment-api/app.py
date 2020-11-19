from flask import Flask, jsonify, request
from filter import classify_tweet_relevance
from sentiment_analysis import predict_sentiment
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

global mongo
mongo = PyMongo(app)


@app.route('/')
def hello():
    return 'Hello, world!'


@app.route('/filter', methods=['POST'])
def filter_tweet():
    content = request.json
    tweet = content['tweet']

    label,_ = classify_tweet_relevance(tweet)
    return jsonify(relevant=label)


@app.route('/predict', methods=['POST'])
def predict():
    content = request.json
    tweet = content['tweet']

    return jsonify(sentiment=predict_sentiment(tweet))


@app.route('/filter-predict', methods=['POST'])
def filter_predict():
    content = request.json
    tweet = content['tweet']

    is_relevant, processed_tweet = classify_tweet_relevance(tweet)
    # Don't calculate sentiment if the tweet is not relevant
    if not is_relevant:
        return jsonify(relevant=is_relevant, sentiment=None)

    sentiment = predict_sentiment(processed_tweet, tweet_preprocessed=True)
    return jsonify(relevant=is_relevant, sentiment=sentiment)


if __name__ == '__main__':
    app.run('0.0.0.0')
