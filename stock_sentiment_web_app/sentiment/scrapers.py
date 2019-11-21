import tweepy
import environ
import re
from .models import Stock, Tweet
from textblob import TextBlob

env = environ.Env()


class TwitterScraper:

    def __init__(self):
        self.stocks = Stock.objects.all()
        self.twitter = self.connect_to_api()

    def connect_to_api(self):
        auth = tweepy.OAuthHandler(env('TWITTER_CONSUMER_KEY'), env('TWITTER_CONSUMER_SECRET'))
        auth.set_access_token(env('TWITTER_ACCESS_KEY'), env('TWITTER_ACCESS_SECRET'))
        return tweepy.API(auth)

    def scrape_for_stock(self, stock):
        # TODO: For later version scrape tweets using the since_id param, not just the latest 100
        for tweet in tweepy.Cursor(self.twitter.search, q="$" + stock.ticker,
                                   count=10, include_entities=True,
                                   result_type='recent', lang='en',
                                   tweet_mode="extended").items(10):
            tweet_data = {
                'text': tweet.full_text,
                'tweet_id': tweet.id_str,
                'created_at': tweet.created_at,
                'username': tweet.user.name,
                'retweets': tweet.retweet_count,
                'sentiment': TextBlob(tweet.full_text).sentiment.polarity
            }

            self.save_tweet(stock, tweet_data)

    def save_tweet(self, stock, tweet_data):
        tweet = Tweet(**tweet_data)
        tweet.save()
        tweet.stocks.add(stock)

    def scrape_for_db_stocks(self):
        # fetch the tweets for each stock
        for stock in self.stocks:
            self.scrape_for_stock(stock)




