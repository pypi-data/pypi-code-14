from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.model.Obj import Obj
from SeasObjects.rdf.Resource import Resource

from rdflib import XSD

import traceback


class Coordinates(Obj):
	
	def __init__(self, uri = None, latitude = None, longitude = None, altitude = None):
		Obj.__init__(self, uri)
		self.latitude = latitude
		self.longitude = longitude
		self.altitude = altitude
		self.setType(RESOURCE.SEAS_COORDINATES);
	
	def hasLongitude(self):
		return self.longitude is not None
	
	def setLongitude(self, l):
		self.longitude = l
	
	def getLongitude(self):
		return self.longitude
	
	def hasLatitude(self):
		return self.latitude is not None
	
	def setLatitude(self, l):
		self.latitude = l
	
	def getLatitude(self):
		return self.latitude
	
	def hasAltitude(self):
		return self.altitude is not None
	
	def setAltitude(self, a):
		self.altitude = a
	
	def getAltitude(self):
		return self.altitude
	
	def serialize(self, model):
		coordinates = super(Coordinates, self).serialize(model)
		
		if self.hasLatitude():
			coordinates.addProperty(model.createProperty( PROPERTY.GEO_LAT ), model.createTypedLiteral(self.getLatitude(), XSD.double))

		if self.hasLongitude():
			coordinates.addProperty(model.createProperty( PROPERTY.GEO_LONG ), model.createTypedLiteral(self.getLongitude(), XSD.double))

		if self.hasAltitude():
			coordinates.addProperty(model.createProperty( PROPERTY.GEO_ALT ), model.createTypedLiteral(self.getAltitude(), XSD.double))

		return coordinates
	
	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				coordinates = Coordinates(resource.toString())
			else:
				coordinates = Coordinates()
			coordinates.clearTypes()
			
			for statement in resource.findProperties():
				# parse statement
				coordinates.parse(statement);
			
			return coordinates
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
			
			# latitude
			if predicate == PROPERTY.GEO_LAT:
				try:
					self.setLatitude(statement.getDouble())
				except:
					print "Unable to interpret geo:lat value as literal double."
					traceback.print_exc()
				return
	
			# longitude
			if predicate == PROPERTY.GEO_LONG:
				try:
					self.setLongitude(statement.getDouble());
				except:
					print "Unable to interpret geo:long value as literal double."
					traceback.print_exc()
				return
			
			# altitude
			if predicate == PROPERTY.GEO_ALT:
				try:
					self.setAltitude(statement.getDouble());
				except:
					print "Unable to interpret geo:alt value as literal double."
					traceback.print_exc()
				return
	
			# pass on to Object
			super(Coordinates, self).parse(statement)
	