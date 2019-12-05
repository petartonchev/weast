from django.shortcuts import render
from django.db.models import Avg
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

from stock_sentiment_web_app.utils.decorators import superuser_only
from .models import Stock, Tweet
import time
from .scrapers import TwitterScraper
import datetime


# Create your views here.

def index(request):
    stocks = Stock.objects.all()
    context = {'stocks': stocks}
    return render(request, 'sentiment/index.html', context)


def get_stock_sentiment(request, stock_id):
    stock = Stock.objects.get(pk=stock_id)
    tweets = stock.tweet_set.all()
    stock_summary = stock.stocksummary_set.latest('date')
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    month = datetime.timedelta(days=30)
    month_ago = datetime.datetime.now() - month
    month_ago = month_ago.strftime("%Y-%m-%d")
    price_trend = [[1572825600000, 2.56729218e+02],
                   [1572912000000, 2.56360352e+02],
                   [1572998400000, 2.56470001e+02],
                   [1573084800000, 2.59429993e+02],
                   [1573171200000, 2.60140015e+02],
                   [1573430400000, 2.62200012e+02],
                   [1573516800000, 2.61959991e+02],
                   [1573603200000, 2.64470001e+02],
                   [1573689600000, 2.62640015e+02],
                   [1573776000000, 2.65760010e+02],
                   [1574035200000, 2.67100006e+02],
                   [1574121600000, 2.66290009e+02],
                   [1574208000000, 2.63190002e+02],
                   [1574294400000, 2.62010010e+02],
                   [1574380800000, 2.61779999e+02],
                   [1574640000000, 2.66369995e+02],
                   [1574726400000, 2.64290009e+02],
                   [1574812800000, 2.67839996e+02],
                   [1574985600000, 2.67250000e+02],
                   [1575244800000, 2.64160004e+02],
                   [1575331200000, 2.59450012e+02]];

    sentiment_trend = [[1572825600000, 0.7],
                       [1572912000000, -0.7],
                       [1572998400000, 0.2],
                       [1573084800000, -0.4],
                       [1573171200000, 0.7],
                       [1573430400000, 0.2],
                       [1573516800000, 0.1],
                       [1573603200000, 0.9],
                       [1573689600000, -1],
                       [1573776000000, 0.5],
                       [1574035200000, -0.78],
                       [1574121600000, -0.7],
                       [1574208000000, 0.1],
                       [1574294400000, 0.7],
                       [1574380800000, 0.4],
                       [1574640000000, -0.7],
                       [1574726400000, 0.0],
                       [1574812800000, 0.43],
                       [1574985600000, -0.0],
                       [1575244800000, -0.2],
                       [1575331200000, 0.7]];

    context = {'sentiment': stock_summary.avg_sentiment,

               'stock': stock,
               'tweets': tweets,
               'price_trend': price_trend,
               'sentiment_trend': sentiment_trend}

    return render(request, 'sentiment/show_sentiment.html', context)


@superuser_only
def scrape_data(request):
    TwitterScraper().scrape_for_db_stocks()
    messages.add_message(request, messages.INFO, "Scrape completed")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
