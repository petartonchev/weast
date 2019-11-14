from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SentimentConfig(AppConfig):
    name = 'stock_sentiment_web_app.sentiment'
    verbose_name = _("Sentiment")
