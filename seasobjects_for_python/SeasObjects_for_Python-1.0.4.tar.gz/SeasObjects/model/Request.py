from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.Tools import Tools

from SeasObjects.model.Message import Message
from SeasObjects.rdf.Resource import Resource

import traceback
import sys
from rdflib import URIRef

class Request(Message):

	def __init__(self, uri = None):
		Message.__init__(self, uri)
		self.setType(RESOURCE.SEAS_REQUEST)
		
	def serialize(self, model):
		r = super(Request, self).serialize(model)
		return r
	
	def fromString(self, data, serialization):
		try:
			return Request.parse(Tools().getResourceByType(RESOURCE.SEAS_REQUEST, Tools().fromString(data, serialization)));
		except:
			print "Unable to parse Request from the given string."
			traceback.print_exc() 
			return None
	
	def parse(self, resource):
		if isinstance(resource, Resource):
			if resource is None:
				raise NullPointerException("Unable to parse null to Request.")
			
			if not resource.isAnon():
				request = Request(resource.toString())
			else:
				request = Request()
			request.clearTypes()
	
			for statement in resource.findProperties():
				# parse statement
				request.parse(statement);
	
			return request
		
		else:
			# pass on to Message
			super(Request, self).parse(resource);
