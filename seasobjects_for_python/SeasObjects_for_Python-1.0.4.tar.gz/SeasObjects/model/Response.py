from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.Tools import Tools

from SeasObjects.rdf.Resource import Resource
from SeasObjects.model.Message import Message

class Response(Message):
	
	def __init__(self, uri = None):
		Message.__init__(self, uri)
		self.setType(RESOURCE.SEAS_RESPONSE)

	def serialize(self, model):
		resource = super(Response, self).serialize(model)

		return resource

	def fromString(self, data, serialization):
		try:
			return self.parse(Tools().getResourceByType(RESOURCE.SEAS_RESPONSE, Tools().fromString(data, serialization)))
		except:
			print "Unable to parse Response from the given string."
			traceback.print_exc() 
			return None
	
	def parse(self, resource):
		if isinstance(resource, Resource):
			if resource == None:
				raise NullPointerException("Unable to parse null to Response.")
	
			if not resource.isAnon():
				response = Response(resource.toString())
			else:
				response = Response()
			response.clearTypes()
	
			for statement in resource.findProperties():
				# parse statement
				response.parse(statement)
	
			return response
		
		else:
			statement = resource
			
			# pass on to Message
			super(Response, self).parse(statement);
