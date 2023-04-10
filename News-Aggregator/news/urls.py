from django.urls import path
from news.views import scrape, news_list,rss_scrape
urlpatterns = [
  path('scrape/', scrape, name="scrape"),
  path('rss_scrape/', rss_scrape, name="rss_scrape"),
  path('', news_list, name="home"),
]