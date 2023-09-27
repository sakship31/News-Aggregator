from django.urls import path
from news.views import scrape, news_list
urlpatterns = [
  path('scrape/<str:name>', scrape, name="scrape"),
  path('', news_list, name="home"),
]