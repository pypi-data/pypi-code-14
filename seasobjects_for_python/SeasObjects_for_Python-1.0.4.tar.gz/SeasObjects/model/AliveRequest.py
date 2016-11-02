from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.Tools import Tools
from SeasObjects.rdf.Resource import Resource

from SeasObjects.model.Request import Request


class AliveRequest(Request):
	
	def __init__(self, uri = None):
		Request.__init__(self, uri)
		self.setType(RESOURCE.SEAS_ALIVEREQUEST)
	
	def serialize(self, model):
		request = super(AliveRequest, self).serialize(model)
		
		return request
	
	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				e = AliveRequest(resource.toString())
			else:
				e = AliveRequest()
			e.clearTypes()

			for statement in resource.findProperties():
				# pass on to Object
				e.parse(statement)
			return e
		
		else:
			statement = resource
			super(AliveRequest, self).parse(statement)
		

	def fromString(self, data, serialization):
		m = Tools().fromString(data, serialization)
		res = Tools().getResourceByType(RESOURCE.SEAS_ALIVEREQUEST, m)
		return self.parse(res)
		