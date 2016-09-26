from datetime import datetime, timedelta

try:
    from urlparse import urljoin, parse_qs, urlparse
except ImportError:
    from urllib.parse import urljoin, parse_qs, urlparse

import requests

class TokenMissingException(IOError):
    """No token has been defined for making API requests"""


class Query(object):
    def __init__(self):
        self.all_terms = None
        self.some_terms = None
        self.phrase = None
        self.exclude = None
        self.site_type = None
        self.language = None
        self.site = None
        self.title = None
        self.body_text = None
        self.is_first = None

    def query_string(self):
        qs = []
        if self.all_terms:
            qs.append(" AND ".join(self.all_terms))
        if self.some_terms:
            qs.append(" OR ".join(self.some_terms))
        if self.phrase:
            qs.append('"%s"' % self.phrase)
        if self.exclude:
            qs.append("-(%s)" % self.exclude)
        if self.site_type:
            if type(self.site_type) is list:
                qs.append(" OR ".join("site_type:%s" % site_type for site_type in self.site_type))
            else:
                qs.append("site_type:%s" % self.site_type)
        if self.language:
            if type(self.language) is list:
                qs.append(" OR ".join("language:%s" % language for language in self.language))
            else:
                qs.append("language:%s" % self.language)
        if self.site:
            if type(self.site) is list:
                qs.append(" OR ".join("site:%s" % site for site in self.site))
            else:
                qs.append("site:%s" % self.site)
        if self.title:
            qs.append("title:%s" % self.title)
        if self.body_text:
            qs.append("text:%s" % self.body_text)
        if self.is_first:
            qs.append("is_first:true")
        return " AND ".join("(%s)" % term for term in qs)

    def __str__(self):
        return self.query_string()

class Response(object):
    """Webhose response. Usually contains a list of posts
    """

    def __init__(self, response, session):
        self.response = response
        self.session = session
        self.total = self.response.json()['totalResults']
        self.next = urljoin(self.response.url, self.response.json()['next'])
        self.next_ts = self.extract_next_ts()
        self.left = self.response.json()['requestsLeft']
        self.more = self.response.json()['moreResultsAvailable']
        self.posts = []
        for post in self.response.json()['posts']:
            self.posts.append(Post(post))

    def extract_next_ts(self):
        resource = self.response.json()['next']
        parsed = urlparse(resource)
        params = parse_qs(parsed.query)
        return params['ts'][0]

    def get_next(self):
        return self.session.get(self.next)

    def __iter__(self):
        response = self
        while True:
            for post in response.posts:
                yield post
            if response.more == 0:
                break
            response = response.get_next()
            self.total = response.total
            self.next = response.next
            self.left = response.left
            self.more = response.more
            self.posts = response.posts
            self.next_ts = response.next_ts


class Thread(object):
    """Information about the thread to which the post belongs
    """

    def __init__(self, thread):
        self.uuid = thread["uuid"]
        self.url = thread["url"]
        self.site_full = thread["site_full"]
        self.site = thread["site"]
        self.site_section = thread.get("site_section")
        self.section_title = thread.get("section_title")
        self.title = thread["title"]
        self.title_full = thread.get("title_full", self.title)
        self.published = thread["published"]
        self.published_parsed = parse_iso8601(thread["published"])
        self.replies_count = thread["replies_count"]
        self.participants_count = thread["participants_count"]
        self.site_type = thread["site_type"]
        self.country = thread.get("country")
        self.spam_score = thread["spam_score"]
        self.main_image = thread["main_image"]
        self.performance_score = thread["performance_score"]


class Post(object):
    """Convenience class for post properties
    """

    def __init__(self, post):
        self.uuid = post["uuid"]
        self.url = post["url"]
        self.title = post["title"]
        self.author = post["author"]
        self.text = post["text"]
        self.published = post["published"]
        self.published_parsed = parse_iso8601(post["published"])
        self.crawled = post["crawled"]
        self.crawled_parsed = parse_iso8601(post["crawled"])
        self.ord_in_thread = post["ord_in_thread"]
        self.language = post["language"]
        self.external_links = post.get("external_links")
        self.persons = post["entities"]["persons"]
        self.locations = post["entities"]["locations"]
        self.organizations = post["entities"]["organizations"]
        self.thread = Thread(post["thread"])


class Session(object):
    """Requests Session, plus additional config
    """

    def __init__(self, token=None):
        self.session = requests.Session()
        self.token = token

    def get(self, url):
        response = self.session.get(url)
        return Response(response, self)

    def search(self, query, token=None, since=None):
        if token is None and self.token is None:
            raise TokenMissingException("No token defined for webhose API request")

        if type(query) is Query:
            query = query.query_string()

        params = {
            "q": query,
            "token": token or self.token
        }

        if since:
            params['ts'] = since

        response = self.session.get("http://webhose.io/search", params=params)
        if response.status_code != 200:
            raise Exception(response.text)
        return Response(response, self)


def parse_iso8601(str_date):
    dt = datetime.strptime(str_date[:-10], "%Y-%m-%dT%H:%M:%S")
    offset = timedelta(hours=int(str_date[24:26]), minutes=int(str_date[27:29])) * (1 if str_date[23] == '+' else -1)
    return dt - offset

__session = Session()


def config(token):
    __session.token = token


def search(query, token=None, since=None):
    return __session.search(query, token, since=since)


def get(url):
    return __session.get(url)
