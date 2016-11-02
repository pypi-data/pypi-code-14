from SeasObjects.common.RESOURCE import RESOURCE

from SeasObjects.model.Ability import Ability
from SeasObjects.rdf.Resource import Resource

class Availability(Ability):

	def __init__(self, uri = None):
		Ability.__init__(self, uri)
		self.setType(RESOURCE.SEAS_AVAILABILITY);
		
	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				availability = Availability(resource.toString());
			else:
				availability = Availability();
			availability.clearTypes()
	
			for i in resource.findProperties():
						# parse statement
				availability.parse(i)

			return availability
