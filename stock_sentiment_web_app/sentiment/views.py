from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from stock_sentiment_web_app.utils.decorators import superuser_only
from .models import Stock, Tweet, IndustrySector, IndustrySectorSummary
from .scrapers import TwitterScraper
from .services import Statistics


# Create your views here.

def index(request):
    stocks = Stock.objects.all()
    sectors = IndustrySector.objects.all()
    tree = []

    for sector in sectors:

        try:
            summary = IndustrySectorSummary.objects.filter(sector_id=sector.id).latest('date')
        except IndustrySectorSummary.DoesNotExist:
            continue

        node = {
            "name": sector.name,
            "value": round(summary.avg_sentiment,2),
            "id": str(sector.id),
            "color": '#F60239' if summary.avg_sentiment < 0 else '#4c9d49'
        }
        tree.append(node)

    for stock in stocks:
        node = {
            "name": stock.ticker,
            "value": round(stock.stocksummary_set.latest('date').avg_sentiment,2),
            "parent": str(stock.sector_id),
            "color": '#F60239' if stock.stocksummary_set.latest('date').avg_sentiment < 0 else '#4c9d49'
        }
        tree.append(node)

    context = {'stocks': stocks, "sector_tree": tree}
    return render(request, 'sentiment/index.html', context)


def get_stock_sentiment(request, stock_id):
    stock = Stock.objects.get(pk=stock_id)
    tweets = stock.tweet_set.all()
    stock_summary = stock.stocksummary_set.latest('date')
    sentiment_trend = Statistics.get_sentiment_trend(stock)

    context = {
        'sentiment': round(stock_summary.avg_sentiment, 2),
        'stock': stock,
        'tweets': tweets,
        'sentiment_trend': sentiment_trend
    }

    return render(request, 'sentiment/show_sentiment.html', context)

@superuser_only
def scrape_data(request):
    TwitterScraper().scrape_for_db_stocks()
    messages.add_message(request, messages.INFO, "Scrape completed")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
