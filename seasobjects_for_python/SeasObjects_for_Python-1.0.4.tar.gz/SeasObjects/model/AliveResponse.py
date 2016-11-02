from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.Tools import Tools
from SeasObjects.rdf.Resource import Resource
from SeasObjects.model.Response import Response

import traceback


class AliveResponse(Response):
	
	def __init__(self, uri = None):
		Response.__init__(self, uri)
		self.setType(RESOURCE.SEAS_ALIVERESPONSE)
	
	def fromString(self, data, serialization):
		try:
			return AliveResponse().parse(Tools().getResourceByType(RESOURCE.SEAS_ALIVERESPONSE, Tools().fromString(data, serialization)))
 		except:
			print "Unable to parse AliveResponse from the given string."
			traceback.print_exc() 
			return None
	
	def serialize(self, model):
		return super(AliveResponse, self).serialize(model)
		
	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				aliveresp = AliveResponse(resource.toString())
			else:
				aliveresp = AliveResponse()
			aliveresp.clearTypes()

			for statement in resource.findProperties():
				# parse statement
				aliveresp.parse(statement)
	
			return aliveresp
		
		else:
			# pass on to Response
			super(AliveResponse, self).parse(resource)

