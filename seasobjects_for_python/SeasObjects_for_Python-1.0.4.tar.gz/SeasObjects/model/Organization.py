from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.rdf.Resource import Resource

from SeasObjects.model.Entity import Entity

import traceback


class Organization(Entity):

	def __init__(self, uri = None):
		Entity.__init__(self, uri)
		self.setType(RESOURCE.SEAS_ORGANIZATION)

	def serialize(self, model):
		organzization = super(Organization, self).serialize(model)
		return organzization

	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				organzization = Organization(resource.toString())
			else:
				organzization = Organization()
			organzization.clearTypes()
	
			for statement in resource.findProperties():
				# parse statement
				organzization.parse(statement);
	
			return organzization
		
		else:
			statement = resource

			# pass on to Entity
			super(Entity, self).parse(statement)

