from django.shortcuts import render
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline
import requests
import feedparser
from datetime import datetime

feed_url = 'https://www.theonion.com/rss'

# Scrage web feed


def scrape(request):

    session = requests.Session()
    session.headers = {
        "User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    # the onion.com  is unstable on his class names , they're using random pregenerated class names that changes
    # in other hand the guardian has static class names and we cand trust them for a long time
    url = "https://www.theguardian.com/world"
    content = session.get(url).content
    soup = BSoup(content, "html.parser")
    News = soup.find_all('div', {"class": "fc-item__container"})
    is_there_any_new_feed = update_scrap_headline(News)
    request.session['new_feeds'] = is_there_any_new_feed
    return redirect("../")


def update_scrap_headline(News):
    print(len(News))
    is_there_any_new_feed = False
    for article in News:
        # Extracting the image source
        image_src = article.find(
            'div', {'class': 'fc-item__image-container'}).find('img')['src']
        # Extracting the title, link and body
        title = article.find('span', {'class': 'js-headline-text'}).text
        link = article.find('a', {'class': 'fc-item__link'})['href']
        body = article.find(
            'div', {'class': 'fc-item__standfirst'}).text.strip()
        if not headline_is_exists(link):
            is_there_any_new_feed = True
            new_headline = Headline()
            new_headline.title = title
            new_headline.url = link
            new_headline.image = image_src
            new_headline.date = "undefined date"
            new_headline.save()

    return is_there_any_new_feed


# Read the RSS feed
def rss_scrape(request):
    feed = feedparser.parse(feed_url)
    is_there_any_new_feed = update_rss_headlines(feed)
    # Set a value in the session
    request.session['new_feeds'] = is_there_any_new_feed
    return redirect("../")


def news_list(request):
    # Get the value from the session using the parameter
    new_feed = request.session.get("new_feeds")
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
        'new_feed': new_feed
    }
    request.session['new_feeds'] = False
    return render(request, "news/home.html", context)


# update headlines to DB
def update_rss_headlines(feed):
    is_there_any_new_feed = False
    print(headline_is_exists("vlowblow"))
    print("Feeds len = {}".format(len(feed.entries)))

    for entry in feed.entries:
        if not headline_is_exists(entry.link):
            is_there_any_new_feed = True
            new_headline = Headline()
            new_headline.title = entry.title
            new_headline.url = entry.link
            soup = BSoup(entry.summary, 'html.parser')
            img_src = soup.find('img')['src']
            new_headline.image = img_src
            published_date = datetime(*entry.published_parsed[:6])
            published_date_str = published_date.strftime('%Y-%m-%d %H:%M:%S')
            new_headline.date = published_date_str
            new_headline.save()
    return is_there_any_new_feed


# check if headline not exist in our DB
def headline_is_exists(entrylink):
    return Headline.objects.filter(url=entrylink).exists()
