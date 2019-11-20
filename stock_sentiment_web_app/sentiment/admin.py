from django.contrib import admin

from .models import Tweet,Stock
# Register your models here.
admin.site.register([Tweet, Stock])
