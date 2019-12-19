import tweepy
import environ
from django.core.exceptions import ValidationError
import requests
from .models import Stock, Tweet
from textblob import TextBlob
from datetime import datetime, timedelta
import operator

env = environ.Env()


class TwitterScraper:

    def __init__(self):
        self.NUM_TWEETS_PER_FETCH = 100
        self.ANALYSER_API = 'https://api-moodstock.herokuapp.com'
        self.stocks = Stock.objects.all()
        self.twitter = self.connect_to_api()
        self.yesterday_date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

    def connect_to_api(self):
        auth = tweepy.OAuthHandler(env('TWITTER_CONSUMER_KEY'), env('TWITTER_CONSUMER_SECRET'))
        auth.set_access_token(env('TWITTER_ACCESS_KEY'), env('TWITTER_ACCESS_SECRET'))
        return tweepy.API(auth)

    def scrape_for_db_stocks(self):
        # fetch the tweets for each stock
        for stock in self.stocks:
            self.scrape_for_stock(stock)

    def scrape_for_stock(self, stock):
        search_query = "${} since:{}".format(stock.ticker, self.yesterday_date)

        for tweet in tweepy.Cursor(self.twitter.search,
                                   q=search_query,
                                   count=self.NUM_TWEETS_PER_FETCH,
                                   # Contains some useful info in the entities like what are the other stocks
                                   # in the tweet so we might use it in the future
                                   include_entities=True,
                                   result_type='recent',  # fetch only the most recent tweets
                                   lang='en',  # our sentiment model works with English only
                                   tweet_mode="extended"
                                   ).items(self.NUM_TWEETS_PER_FETCH):

            is_relevant, sentiment = self.filter_analyse_tweet(tweet.full_text)
            # Save only if relevant and has sentiment
            if is_relevant and sentiment is not None:
                tweet_data = {
                    'text': tweet.full_text,
                    'tweet_id': tweet.id_str,
                    'created_at': tweet.created_at,
                    'username': tweet.user.name,
                    'retweets': tweet.retweet_count,
                    'sentiment': sentiment
                }

                corresponding_stocks = self.get_stocks_from_tweet_symbols(tweet.entities['symbols'])
                self.save_tweet(corresponding_stocks, tweet_data)

    def get_stocks_from_tweet_symbols(self, symbols):
        # get the text of the symbols only
        symbols = map(lambda symbol: symbol['text'].upper(), symbols)

        return self.stocks.filter(ticker__in=symbols)

    def save_tweet(self, stocks, tweet_data):
        # Don't save the tweet if for some reason no stocks are associated with it.
        if not stocks:
            return

        tweet = Tweet(**tweet_data)
        try:
            tweet.validate_unique()
            tweet.save()

            for stock in stocks:
                tweet.stocks.add(stock)
        except ValidationError:
            # This error will be thrown if the tweet has already been inserted so just ignore the exception and continue
            pass

    def filter_analyse_tweet(self, full_text):
        try:
            response = requests.post(self.ANALYSER_API + '/filter-predict', json={"tweet": full_text}, timeout=30.0)

            if response.ok:
                print(response.json())
                result = response.json()
                return result['relevant'], result['sentiment']
            else:
                return False, None
        except:
            return False, None
