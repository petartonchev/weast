import datetime
from django.utils import timezone


class Statistics:

    @staticmethod
    def get_sentiment_trend(stock):
        month = datetime.timedelta(days=30)
        month_ago = datetime.datetime.now() - month
        month_ago = month_ago.strftime("%Y-%m-%d")
        sentiment_trend = stock.stocksummary_set.filter(date__gte=month_ago).all().values_list('date', 'avg_sentiment')

        def convert_date_to_timestamp(daily_summary):
            date, sentiment = daily_summary
            # Convert to timestamp in milliseconds
            timestamp = int(timezone.datetime.timestamp(date) * 1000)
            return [timestamp, sentiment]

        return list(map(convert_date_to_timestamp, sentiment_trend))
