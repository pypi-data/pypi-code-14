import urlnorm, urlparse, re

class ResourceRequest:

  def __init__(self, link, depth, crawl_id, depth_limit, parent_uri=None):
    self.link = urlnorm.norm(urlparse.urljoin(parent_uri if parent_uri else '', link))
    self.link = self.link.split('#')[0]

    self.attempts = 0
    self.crawl_id = crawl_id
    self.depth = depth
    self.depth_limit = depth_limit

  def addAttempt(self):
    self.attempts += 1

  def id(self):
    return self.crawl_id + ':' + self.link

  def __hash__(self):
    return hash(self.id())

  def __eq__(self, other):
    if isinstance(other, self.__class__):
        return ((self.link == other.link) and 
          (self.crawl_id == other.crawl_id))
    return False
