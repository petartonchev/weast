from djongo import models


class Stock(models.Model):
    ticker = models.CharField(max_length=10)

    class Meta:
        abstract = True


class Tweet(models.Model):
    stocks = models.EmbeddedModelField(
        model_container=Stock
    )

    text = models.TextField()
    created_at = models.DateTimeField(blank=True)
    username = models.CharField(max_length=255)
    retweets = models.PositiveIntegerField()
    sentiment = models.FloatField()
