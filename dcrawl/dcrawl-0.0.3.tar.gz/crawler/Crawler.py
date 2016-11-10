from crawler.ResourceRequest import ResourceRequest
import urlnorm, urlparse, time


class Crawler(object):
  depth_limit = 20
  _stop_on_empty = False
  retry_limit = 2

  def __init__(self, queue, urlset, http):
    self.queue = queue
    self.urlset = urlset
    self.throttle_control = None
    self.http = http
    self.processors = []

  def should_follow(self, resource_request):
    return resource_request.id() not in self.urlset and resource_request.depth < resource_request.depth_limit

  def add_resource_request(self, resource_request):
    if self.should_follow(resource_request):
      self.queue.send([resource_request])
      self.urlset.add(resource_request.id())

  def add_response_processor(self, processor):
    self.processors.append(processor)

  def process(self, url, response):
    for processor in self.processors:
      try:
        processor.process(self, url, response)
      except AttributeError:
        pass

  def tick(self):
    for processor in self.processors:
      try:
        processor.tick()
      except AttributeError:
        pass

  def close(self):
    for processor in self.processors:
      try:
        processor.close()
      except AttributeError:
        pass

  def follow(self, response, newRequest):
    return newRequest.id() not in self.urlset and newRequest.depth < self.depth_limit and newRequest.follow(response)

  def crawl(self):
    try:
      while True:
        self.tick()
        if (self.throttle_control):
          time.sleep(self.throttle_control)

        crawlRequest = self.queue.get()
        if crawlRequest is None:
          print "Queue empty sleeping"
          time.sleep(1)
          continue
        try:
          print "Crawling ", crawlRequest.link, 'attempt',crawlRequest.attempts,
          print 'crawl id',crawlRequest.crawl_id, 'depth', crawlRequest.depth
          response = self.http.get(crawlRequest.link)

          self.process(crawlRequest, response)

        except Exception as e:
          #Increment attempts and forward this request on
          crawlRequest.addAttempt()
          if (crawlRequest.attempts < self.retry_limit):
            self.queue.send([crawlRequest])
          print "Error on link - retry", e

    finally:
      self.close()