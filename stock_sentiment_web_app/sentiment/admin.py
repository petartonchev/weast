from django.contrib import admin
from django.utils.html import format_html

from .models import Tweet,Stock
# Register your models here.


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['ticker', 'company']
    change_list_template = "sentiment/stock_changelist.html"


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['text', 'sentiment', 'retweets', 'created_at', 'stocks_display']

    def stocks_display(self, obj):
        return ", ".join([
            stock.ticker for stock in obj.stocks.all()
        ])

    list_per_page = 5
    stocks_display.short_description = "Stocks"
