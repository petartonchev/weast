from apscheduler.schedulers.background import BackgroundScheduler
from stock_sentiment_web_app.sentiment.scrapers import TwitterScraper


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(start_tweet_scraper, 'interval', hours=1)
    scheduler.start()


# Helper method since add_job doesn't accept class methods
def start_tweet_scraper():
    TwitterScraper().scrape_for_db_stocks()
