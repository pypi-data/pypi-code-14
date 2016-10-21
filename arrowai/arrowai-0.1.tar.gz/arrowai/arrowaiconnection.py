import requests
# POST with JSON 
import json

class ArrowAIConnection(object):
	url = "http://localhost:8000/"

	def __init__(self, key, name):
		self.key = key
		self.name = name

	def getKey(self):
		return self.key

	def getName(self):
		return self.name

	def sendApiRequest(self, urlReq, data):
		print "sending Request"
		print self.url + urlReq
		r = requests.post(self.url + urlReq, data=json.dumps(data))
		print r.json()
		return r.json()
