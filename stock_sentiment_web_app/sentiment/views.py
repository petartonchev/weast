from django.shortcuts import render
from django.http import HttpResponse
import time


# Create your views here.

def index(request):
    tickers = ['AAPL', 'AA', 'FB', 'UR']
    context = {'tickers': tickers}
    return render(request, 'sentiment/index.html', context)


def get_stock_sentiment(request, ticker):
    # stock = get_object_or_404(Question, pk=question_id)
    sentiment = 0.6
    tweets = [
        {
            "_id": {
                "$oid": "5dcbefee8aad706ad9976c18"
            },
            "text": "$ES_F #ES #es_f S&amp;P 500 Futures .. Hourly\nBroke neck line! https://t.co/PXX3FtJ6dW",
            "created_at": {
                "date": time.strftime('%Y-%m-%d  %H:%M:%S',
                                      time.strptime("2019-11-13T09:41:19+0000","%Y-%m-%dT%H:%M:%S%z"))
            },
            "user_name": "winner_trader",
            "stock": [
                "$ES"
            ],
            "retweet_count": 0
        },
        {
            "_id": {
                "$oid": "5dcbefee8aad706ad9976c19"
            },
            "text": "Robotic Revolution watch-list from Yahoo.. (By market cap)\n$HON Honeywell International  $182\n$LMT Lockheed Martin\u2026 https://t.co/lHAdl04eOr",
            "created_at": {
                "date": time.strftime('%Y-%m-%d  %H:%M:%S',
                                      time.strptime("2019-11-13T09:41:19+0000", "%Y-%m-%dT%H:%M:%S%z"))

            },
            "user_name": "winner_trader",
            "stock": [
                "$HON",
                "$LMT"
            ],
            "retweet_count": 1
        },
        {
            "_id": {
                "$oid": "5dcbefee8aad706ad9976c1a"
            },
            "text": "$TSLA Closed with bullish candle after late good headlines . Now levels raised . Stops for long became 340 . target\u2026 https://t.co/SVehy4d3SN",
            "created_at": {
                "date": time.strftime('%Y-%m-%d  %H:%M:%S',
                                      time.strptime("2019-11-13T09:41:19+0000", "%Y-%m-%dT%H:%M:%S%z"))

            },
            "user_name": "winner_trader",
            "stock": [
                "$TSLA"
            ],
            "retweet_count": 9
        }
    ]
    context = {'sentiment': sentiment,
               'ticker': ticker,
               'tweets': tweets}
    return render(request, 'sentiment/show_sentiment.html', context)
