# News-Aggregator
Django project to scrape a news website using Beautiful soup and request module.

A news aggregator is a combination of web crawlers and web applications. 
Both of these technologies have their implementation in Python. 
So, our news aggregator will work in 3 steps:
It scrapes the web for the articles. 
In this Django project, we are scraping a website called theonion 
(We have scraped news articles from 'latest' section of 'www.theonion.com' for demonstration)
Then it stores the article’s images, links, and title.
The stored objects in the database are served to the client. The client gets information in a nice template.

Tech Stack used-
1.Django framework (for web development)
2.Python (used in django framework and web scraping)
3.Beautiful Soup-bs4 (for web scrawling)
4.Request module 
