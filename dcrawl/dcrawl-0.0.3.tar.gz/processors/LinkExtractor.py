import re

from urlparse import urlparse

from bs4 import BeautifulSoup
import chardet

from crawler.ResourceRequest import ResourceRequest

def get_links(raw):
    encoding = chardet.detect(raw)

    if (encoding['encoding']):
      encoding = encoding['encoding']
    else:
      encoding = 'ascii'
    content = unicode(raw, encoding, errors='replace')
    soup = BeautifulSoup(content, "html.parser")

    return [l.get('href') for l in soup.findAll('a') if l.get('href')]

class LinkExtractor(object):
  def __init__(self, should_follow=lambda x: True, should_process=lambda x: True):
    self.should_process = should_process
    self.should_follow = should_follow

  def process(self, crawler, resource_req, response):
    if not self.should_process(response):
      return
    links = get_links(response['body'])
    for link in links:
      req = ResourceRequest(link, 
        depth=resource_req.depth + 1,
        depth_limit=resource_req.depth_limit,
        crawl_id=resource_req.crawl_id,
        parent_uri=resource_req.link)
      if not self.should_follow(req.link):
        continue
      crawler.add_resource_request(req)

  def close(self):
    pass

  def tick(self):
    pass