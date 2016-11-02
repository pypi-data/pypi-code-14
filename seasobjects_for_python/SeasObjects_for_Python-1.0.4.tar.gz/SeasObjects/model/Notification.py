from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.Tools import Tools
from SeasObjects.rdf.Resource import Resource
from SeasObjects.model.Message import Message

from SeasObjects.seasexceptions.NonePointerException import NonePointerException


class Notification(Message):

	def __init__(self, uri = None):
		Message.__init__(self, uri)
		self.setType(RESOURCE.SEAS_NOTIFICATION)
			
	def serialize(self, model):
		return super(Notification, self).serialize(model)

	def fromString(self, data, serialization):
		try:
			return Notification.parse(Tools().getResourceByType(RESOURCE.SEAS_NOTIFICATION, Tools().fromString(data, serialization)))
		except:
			print "Unable to parse Notification from the given string."
			traceback.print_exc()
			return None
	
	def parse(self, resource):
		if resource is None:
			raise NonePointerException("Unable to parse null to Notification.")
		
		if isinstance(resource, Resource):
			if not resource.isAnon():
				notification = Notification(resource.toString())
			else:
				notification = Notification()
			notification.clearTypes()
	
			for statement in resource.findProperties():
				# parse statement
				notification.parse(statement);
	
			return notification

		else:
			# pass on to Message
			super(Notification, self).parse(resource)
