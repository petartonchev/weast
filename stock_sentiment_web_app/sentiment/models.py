from django.db import models


class Stock(models.Model):
    name = models.CharField()
    ticker = models.CharField()


class Tweet(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(blank=True)
    username = models.CharField()
    stocks = models.ManyToManyField(Stock)
    retweets = models.PositiveIntegerField()
