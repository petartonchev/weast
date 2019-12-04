from django.db import models


class IndustrySector(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)

    def __str__(self):
        return self.name


class IndustrySectorSummary(models.Model):
    id = models.BigIntegerField(primary_key=True)
    sector = models.ForeignKey(IndustrySector, on_delete=models.DO_NOTHING)
    avg_sentiment = models.FloatField()
    date = models.DateTimeField()

    class Meta:
        managed = False  # tell Django to don't try creating db schema migration for this model
        db_table = 'sentiment_industrysector_summary'


class Stock(models.Model):
    ticker = models.CharField(max_length=10, blank=False, unique=True)
    company = models.CharField(max_length=50, blank=False)
    sector = models.ForeignKey(IndustrySector, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.company + ' (' + self.ticker + ')'


# An SQL View to aggregate the stocks data
class StockSummary(models.Model):
    id = models.BigIntegerField(primary_key=True)
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    avg_sentiment = models.FloatField()
    date = models.DateTimeField()

    class Meta:
        managed = False  # tell Django to don't try creating db schema migration for this model
        db_table = 'sentiment_stock_summary'


class Tweet(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(blank=True)
    username = models.CharField(max_length=255)
    retweets = models.PositiveIntegerField()
    sentiment = models.FloatField()
    stocks = models.ManyToManyField(Stock)

    # Stores the tweet id from twitter
    tweet_id = models.CharField(max_length=255, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tweet_id'], name="unique-tweets")
        ]

    def __str__(self):
        return self.text
