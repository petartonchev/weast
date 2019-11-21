from django.contrib import admin
from django.utils.html import format_html

from .models import Tweet,Stock
# Register your models here.


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    change_list_template = "sentiment/stock_changelist.html"


admin.site.register([Tweet])
