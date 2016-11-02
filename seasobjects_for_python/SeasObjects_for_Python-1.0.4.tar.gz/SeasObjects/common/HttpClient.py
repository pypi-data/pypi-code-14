import urllib, urllib2
from urlparse import urlparse

class HttpClient(object):
	def __init__(self):
		pass
	
	def sendPost(self, server_uri, payload, content_type = "text/turtle", accept_type = "text/turtle"):
		response = ""
		headers = { "content-type" : content_type, 'accept': accept_type }
		try:
			req = urllib2.Request(server_uri, payload, headers)
			# use a 5s timeout
			filehandle = urllib2.urlopen(req, timeout = 5)
			if filehandle is not None:
				data = filehandle.read()
				response = data
		except:
			print "Failed in contacting", server_uri
			print sys.exc_info()[1]
 			response = None
 		finally:
 			return response

	def sendGet(self, server_uri):
		response = ""
		try:
			req = urllib2.Request(server_uri)
			# use a 5s timeout
			filehandle = urllib2.urlopen(req, timeout = 5)
			if filehandle is not None:
				data = filehandle.read()
				response = data
		except:
			print "Failed in contacting", server_uri
			print sys.exc_info()[1]
 			response = None
 		finally:
 			return response
 		
		return response
	