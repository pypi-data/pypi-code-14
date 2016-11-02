from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.model.Obj import Obj
from SeasObjects.model.Coordinates import Coordinates

from SeasObjects.rdf.Resource import Resource
from SeasObjects.rdf.types import *
from rdflib import XSD

import traceback

class Location(Obj):

	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.country = None
		self.city = None
		self.zipCode = None
		self.streetAddress = None
		self.zone = None
		self.coordinates = None
		self.setType(RESOURCE.SEAS_LOCATION)

	def hasCoordinates(self):
		return self.coordinates is not None
	
	def getCoordinates(self):
		return self.coordinates

	def setCoordinates(self, coordinates):
		self.coordinates = coordinates

	def hasCountry(self):
		return self.country is not None
	
	def getCountry(self):
		return self.country

	def setCountry(self, country):
		self.country = country

	def hasCity(self):
		return self.city is not None

	def getCity(self):
		return self.city

	def setCity(self, city):
		self.city = city

	def hasZipCode(self):
		return self.zipCode is not None

	def getZipCode(self):
		return self.zipCode

	def setZipCode(self, zipCode):
		self.zipCode = zipCode

	def hasStreetAddress(self):
		return self.streetAddress is not None

	def getStreetAddress(self):
		return self.streetAddress

	def setStreetAddress(self, streetAddress):
		self.streetAddress = streetAddress

	def hasZone(self):
		return self.zone is not None
	
	def getZone(self):
		return self.zone

	def setZone(self, zone):
		self.zone = zone

	def serialize(self, model):
		resource = super(Location, self).serialize(model)
	
		# coordinates
		if self.hasCoordinates():
			resource.addProperty(model.createProperty( PROPERTY.SEAS_COORDINATES ), self.coordinates.serialize(model))
				
		# country name
		if self.hasCountry():
			resource.addProperty(model.createProperty( PROPERTY.VCARD_COUNTRY_NAME ), self.country)
		
		# locality
		if self.hasCity():
			resource.addProperty(model.createProperty( PROPERTY.VCARD_LOCALITY ), self.city)
		
		# postal code
		if self.hasZipCode():
			resource.addProperty(model.createProperty( PROPERTY.VCARD_POSTAL_CODE ), self.zipCode)
		
		# street address
		if self.hasStreetAddress():
			resource.addProperty(model.createProperty( PROPERTY.VCARD_STREET_ADDRESS ), self.streetAddress)

		# set zone
		if self.hasZone():
			resource.addProperty(model.createProperty( PROPERTY.SEAS_ZONE ), self.zone)

		return resource


	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				location = Location(resource.toString())
			else:
				location = Location()
			location.clearTypes()
			
			for statement in resource.findProperties():
				# parse statement
				location.parse(statement);
			
			return location
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
	
			# country
			if predicate == PROPERTY.VCARD_COUNTRY_NAME:
				try:
					self.setCountry(statement.getString());
				except:
					print "Unable to interpret vcard:country-name value as literal string."
					traceback.print_exc()
				return
	
			# city
			if predicate == PROPERTY.VCARD_LOCALITY:
				try:
					self.setCity(statement.getString())
				except:
					print "Unable to interpret vcard:locality value as literal string."
					traceback.print_exc()
				return
	
			# street-address
			if predicate == PROPERTY.VCARD_STREET_ADDRESS:
				try:
					self.setStreetAddress(statement.getString())
				except:
					print "Unable to interpret vcard:street-address value as literal string."
					traceback.print_exc()
				return
	
			# zipcode
			if predicate == PROPERTY.VCARD_POSTAL_CODE:
				try:
					self.setZipCode(statement.getString())
				except:
					print "Unable to interpret vcard:postal-code value as literal string."
					traceback.print_exc()
				return
	
			# latitude
			if predicate == PROPERTY.SEAS_COORDINATES:
				try:
					self.setCoordinates(Coordinates().parse(statement.getResource()))
				except:
					print "Unable to interpret geo:lat value as literal double."
					traceback.print_exc()
				return
		
			# zone
			if predicate == PROPERTY.SEAS_ZONE:
				try:
					self.setZone(statement.getString());
				except:
					print "Unable to interpret seas:zone value as literal string."
					traceback.print_exc()
				return
	
			# pass on to Object
			super(Location, self).parse(statement)
	
