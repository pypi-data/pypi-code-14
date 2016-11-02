from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.model.Obj import Obj
from SeasObjects.model.Coordinates import Coordinates
from SeasObjects.model.ValueObject import ValueObject

from SeasObjects.rdf.Resource import Resource
from SeasObjects.rdf.types import *
from rdflib import XSD

import traceback

class Ring(Obj):

	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.minRadius = None
		self.maxRadius = None
		self.coordinates = None
		self.setType(RESOURCE.SEAS_RING)

	def hasCoordinates(self):
		return self.coordinates is not None
	
	def getCoordinates(self):
		return self.coordinates

	def setCoordinates(self, coordinates):
		self.coordinates = coordinates

	def hasMinRadius(self):
		return self.minRadius is not None
	
	def getMinRadius(self):
		return self.minRadius

	def setMinRadius(self, r):
		self.minRadius = r

	def hasMaxRadius(self):
		return self.maxRadius is not None
	
	def getMaxRadius(self):
		return self.maxRadius

	def setMaxRadius(self, r):
		self.maxRadius = r

	def serialize(self, model):
		resource = super(Ring, self).serialize(model)
	
		# coordinates
		if self.hasCoordinates():
			resource.addProperty(model.createProperty( PROPERTY.SEAS_COORDINATES ), self.coordinates.serialize(model))
				
		# min radius
		if self.hasMinRadius():
			resource.addProperty(model.createProperty( PROPERTY.SEAS_MINRADIUS ), self.minRadius.serialize(model))
		
		# max radius
		if self.hasMaxRadius():
			resource.addProperty(model.createProperty( PROPERTY.SEAS_MAXRADIUS ), self.maxRadius.serialize(model))
		
		return resource


	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				ring = Ring(resource.toString())
			else:
				ring = Ring()
			ring.clearTypes()
			
			for statement in resource.findProperties():
				# parse statement
				ring.parse(statement);
			
			return ring
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
	
			# latitude
			if predicate == PROPERTY.SEAS_COORDINATES:
				try:
					self.setCoordinates(Coordinates().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:coordinates value as coordinates."
					traceback.print_exc()
				return
		
			if predicate == PROPERTY.SEAS_MINRADIUS:
				try:
					self.setMinRadius(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:minradius value."
					traceback.print_exc()
				return
	
			if predicate == PROPERTY.SEAS_MAXRADIUS:
				try:
					self.setMaxRadius(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:maxradius value."
					traceback.print_exc()
				return
			
			# pass on to Object
			super(Ring, self).parse(statement)
	
