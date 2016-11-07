try:
    from urllib import urlencode
    from urlparse import urlparse, parse_qsl
except ImportError:  # Python3
    from urllib.parse import urlencode, urlparse, parse_qsl

import re
import time

from bs4 import BeautifulSoup
import feedparser


class RelatedNewsScraper(object):

    def __init__(self):
        self.base_url = "https://news.google.com/news"

        self.topics_map = {"world": "w",
                           "us": "n",
                           "elections": "e",
                           "business": "b",
                           "tech": "tc",
                           "entertainment": "e",
                           "sports": "s",
                           "science": "snc",
                           "health": "m"}

    def add_url_params(self, url, new_params):
        """
        Returns the url reformatted with the additional parameters added.
        """
        parsed = urlparse(url)
        params_raw = parsed.query
        params = dict(parse_qsl(params_raw))
        params.update(new_params)
        encoded_params = urlencode(params, doseq=True)
        ncl = None
        if "ncl" in params:
            ncl = params["ncl"]
        new_url = self.base_url + "?" + encoded_params
        return new_url, ncl

    def scrape_latest(self, topic=None):
        """
        Returns a dictionary containing groups of related articles.

        Each group of articles is referenced using a unique identifier. Each
        article in that group is represented as a dictionary with the following
        attributes:
            -title: title of the article
            -source: news source where article is published
            -url: url to the article
            -published: date the article was published

        A topic can optionally be specified. The options are:
            -world
            -US
            -elections
            -tech
            -business
            -entertainment
            -sports
            -science
            -health
        """
        params = {"output": "rss"}

        if topic:
            topic = topic.lower()
            if topic in self.topics_map:
                params["topic"] = self.topics_map[topic]
            else:
                err_str = "Error: topic not valid. Try world, US, elections, tech, "
                err_str += "business, entertainment, sports, science, or health."
                print err_str
                return
        feed_url, _ = self.add_url_params(self.base_url, params)
        feed = feedparser.parse(feed_url)

        data = {}
        for entry in feed["entries"]:
            description = entry["summary"]

            soup = BeautifulSoup(description, "lxml")
            related_url = soup.find("a", href=re.compile("news/more\?"))["href"]
            related_rss, ncl = self.add_url_params(related_url, {"output": "rss"})
            data[ncl] = self.scrape_related(related_rss)

        return data

    def scrape_related(self, feed_url):
        """
        Returns a list of articles, represented as dictionaries with the following
        attributes:
            -title: title of the article
            -source: news source where article is published
            -url: url to the article
            -published: date the article was published
        """
        related_articles = []
        feed = feedparser.parse(feed_url)
        for entry in feed["entries"]:
            article = {}
            link_parsed = urlparse(entry["link"])
            params_raw = link_parsed.query
            params = dict(parse_qsl(params_raw))
            article["url"] = params["url"]
            article["published"] = time.strftime("%m-%d-%Y", entry["published_parsed"])
            title_parts = entry["title"].split(" - ")
            article["title"] = " - ".join(title_parts[:-1])
            article["source"] = title_parts[-1]

            related_articles.append(article)
        return related_articles
