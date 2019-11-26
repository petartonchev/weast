from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class SentimentConfig(AppConfig):
    name = 'stock_sentiment_web_app.sentiment'
    verbose_name = _("Sentiment")

    def ready(self):
        if not settings.DEBUG:
            from . import scheduler  # the import should be local for inheritance reasons
            scheduler.start()
