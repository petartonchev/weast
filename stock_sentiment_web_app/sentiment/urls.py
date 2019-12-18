from django.urls import path
from . import views

app_name = 'sentiment'
urlpatterns = [
    path("", views.index, name='index'),
    path("<int:stock_id>/", views.get_stock_sentiment, name='get_stock_sentiment')
]
