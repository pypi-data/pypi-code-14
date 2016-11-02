from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.model.Obj import Obj

from SeasObjects.rdf.Resource import Resource
from SeasObjects.rdf.types import *
from rdflib import XSD

import traceback

class Zone(Obj):

	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.zoneNUmber = None
		self.setType(RESOURCE.SEAS_ZONE)

	def hasZoneNumber(self):
		return self.zoneNumber is not None
	
	def getZoneNumber(self):
		return self.zoneNumber

	def setZoneNumber(self, zoneNumber):
		self.zoneNumber = zoneNumber

	def serialize(self, model):
		resource = super(Location, self).serialize(model)
	
		# set zone
		if self.hasZoneNumber():
			resource.addProperty(model.createProperty( PROPERTY.SEAS_ZONENUMBER ), self.zoneNumber)

		return resource


	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				z = Zone(resource.toString())
			else:
				z = Zone()
			z.clearTypes()
			
			for statement in resource.findProperties():
				# parse statement
				z.parse(statement);
			
			return z
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
	
			# country
			if predicate == PROPERTY.SEAS_ZONENUMBER:
				try:
					self.setZoneNumber(statement.getString());
				except:
					print "Unable to interpret seas:zoneNumber value as literal string."
					traceback.print_exc()
				return
		
			# pass on to Object
			super(Zone, self).parse(statement)
	
