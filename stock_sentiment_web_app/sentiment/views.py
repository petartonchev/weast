from django.shortcuts import render
from django.db.models import Avg
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

from stock_sentiment_web_app.utils.decorators import superuser_only
from .models import Stock, Tweet
import time
from .scrapers import TwitterScraper


# Create your views here.

def index(request):

    stocks = Stock.objects.all()
    context = {'stocks': stocks}
    return render(request, 'sentiment/index.html', context)


def get_stock_sentiment(request, stock_id):
    stock = Stock.objects.get(pk=stock_id)
    tweets = stock.tweet_set.all()
    stock_summary = stock.stocksummary_set.latest('date')

    context = {'sentiment': stock_summary.avg_sentiment,
               'stock': stock,
               'tweets': tweets}
    return render(request, 'sentiment/show_sentiment.html', context)


@superuser_only
def scrape_data(request):
    TwitterScraper().scrape_for_db_stocks()
    messages.add_message(request, messages.INFO, "Scrape completed")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
