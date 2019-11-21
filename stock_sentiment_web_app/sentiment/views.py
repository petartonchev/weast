from django.shortcuts import render
from django.db.models import Avg
from django.http import HttpResponse
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
    sentiment = tweets.aggregate(Avg('sentiment'))

    context = {'sentiment': sentiment['sentiment__avg'],
               'stock': stock,
               'tweets': tweets}
    return render(request, 'sentiment/show_sentiment.html', context)
