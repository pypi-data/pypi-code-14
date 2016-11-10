import urllib2
import time

class SimpleHttp(object):

  def get(self, req):
    response = urllib2.urlopen(req, timeout=5)
    return {
      'headers' : {k.lower(): v for k, v in response.headers.dict.iteritems()},
      'url' : response.url,
      'status' : response.code,
      'body' : response.read(),
      'accessed' : int(time.time())
    }
