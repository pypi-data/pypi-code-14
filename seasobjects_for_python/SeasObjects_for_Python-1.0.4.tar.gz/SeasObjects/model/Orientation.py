from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.rdf.Resource import Resource
from SeasObjects.model.Obj import Obj
from SeasObjects.model.ValueObject import ValueObject
from SeasObjects.model.Coordinates import Coordinates

from rdflib import XSD
import traceback

class Orientation(Obj):
	
	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.yaw = None
		self.pitch = None
		self.roll = None
		self.setType(RESOURCE.SEAS_ORIENTATION);
	
	def hasYaw(self):
		return self.yaw is not None
	
	def setYaw(self, l):
		self.yaw = l
	
	def getYaw(self):
		return self.yaw
	
	def hasPitch(self):
		return self.pitch is not None
	
	def setPitch(self, l):
		self.pitch = l
	
	def getPitch(self):
		return self.pitch
	
	def hasRoll(self):
		return self.roll is not None
	
	def setRoll(self, a):
		self.roll = a
	
	def getRoll(self):
		return self.roll
		
	def serialize(self, model):
		orientation = super(Orientation, self).serialize(model)
		
		if self.hasPitch():
			orientation.addProperty(model.createProperty( PROPERTY.SEAS_PITCH ), self.getPitch().serialize(model))

		if self.hasYaw():
			orientation.addProperty(model.createProperty( PROPERTY.SEAS_YAW ), self.getYaw().serialize(model))

		if self.hasRoll():
			orientation.addProperty(model.createProperty( PROPERTY.SEAS_ROLL ), self.getRoll().serialize(model))

		return orientation
	
	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				orientation = Orientation(resource.toString())
			else:
				orientation = Orientation()
			orientation.clearTypes()
			
			for statement in resource.findProperties():
				# parse statement
				orientation.parse(statement);
			
			return orientation
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
	
			# pitch
			if predicate == PROPERTY.SEAS_PITCH:
				try:
					self.setPitch(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:pitch value as literal double."
					traceback.print_exc()
				return
	
			# yaw
			if predicate == PROPERTY.SEAS_YAW:
				try:
					self.setYaw(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:yaw value as literal double."
					traceback.print_exc()
				return
			
			# roll
			if predicate == PROPERTY.SEAS_ROLL:
				try:
					self.setRoll(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:roll value as literal double."
					traceback.print_exc()
				return
				
			# pass on to Object
			super(Orientation, self).parse(statement)
	