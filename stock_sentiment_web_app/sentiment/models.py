from django.db import models


class Stock(models.Model):
    ticker = models.CharField(max_length=10, blank=False, unique=True)
    company = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.ticker


class Tweet(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(blank=True)
    username = models.CharField(max_length=255)
    retweets = models.PositiveIntegerField()
    sentiment = models.FloatField()
    stocks = models.ManyToManyField(Stock)

    def __str__(self):
        return self.text
