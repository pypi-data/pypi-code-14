from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.rdf.Resource import Resource

from SeasObjects.model.PhysicalEntity import PhysicalEntity

import traceback

class Person(PhysicalEntity):

	def __init__(self, uri = None):
		PhysicalEntity.__init__(self, uri)
		self.setType(RESOURCE.SEAS_PERSON)

	def serialize(self, model):
		p = super(Person, self).serialize(model)
		return p
	
	def parse(self, resource):
		
		if isinstance(resource, Resource):
			if not resource.isAnon():
				p = Person(resource.toString())
			else:
				p = Person()
			
			for statement in resource.findProperties():
				# parse statement
				p.parse(statement);
	
			return activity
		
		else:
			statement = resource

			# pass on to Object
			super(Person, self).parse(statement)
