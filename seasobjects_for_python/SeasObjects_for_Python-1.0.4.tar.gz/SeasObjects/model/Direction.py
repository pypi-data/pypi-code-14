from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.rdf.Resource import Resource
from SeasObjects.model.Obj import Obj
from SeasObjects.model.ValueObject import ValueObject

from rdflib import XSD
import traceback

class Direction(Obj):
	
	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.bearing = None
		self.heading = None
		self.tracking = None
		self.course = None
		self.setType(RESOURCE.SEAS_DIRECTION);
	
	def hasHeading(self):
		return self.heading is not None
	
	def setHeading(self, l):
		self.heading = l
	
	def getHeading(self):
		return self.heading
	
	def hasBearing(self):
		return self.bearing is not None
	
	def setBearing(self, l):
		self.bearing = l
	
	def getBearing(self):
		return self.bearing
	
	def hasTracking(self):
		return self.tracking is not None
	
	def setTracking(self, a):
		self.tracking = a
	
	def getTracking(self):
		return self.tracking
	
	def hasCourse(self):
		return self.course is not None
	
	def setCourse(self, a):
		self.course = a
	
	def getCourse(self):
		return self.course
	
	def serialize(self, model):
		direction = super(Direction, self).serialize(model)
		
		if self.hasBearing():
			direction.addProperty(model.createProperty( PROPERTY.SEAS_BEARING ), self.getBearing().serialize(model))

		if self.hasHeading():
			direction.addProperty(model.createProperty( PROPERTY.SEAS_HEADING ), self.getHeading().serialize(model))

		if self.hasTracking():
			direction.addProperty(model.createProperty( PROPERTY.SEAS_TRACKING ), self.getTracking().serialize(model))

		if self.hasCourse():
			direction.addProperty(model.createProperty( PROPERTY.SEAS_COURSE ), self.getCourse().serialize(model))

		return direction
	
	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				direction = Direction(resource.toString())
			else:
				direction = Direction()
			direction.clearTypes()
			
			for statement in resource.findProperties():
				# parse statement
				direction.parse(statement);
			
			return direction
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
	
			# bearing
			if predicate == PROPERTY.SEAS_BEARING:
				try:
					self.setBearing(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:bearing value as ValueObject."
					traceback.print_exc()
				return
	
			# heading
			if predicate == PROPERTY.SEAS_HEADING:
				try:
					self.setHeading(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:heading value as ValueObject."
					traceback.print_exc()
				return
			
			# tracking
			if predicate == PROPERTY.SEAS_TRACKING:
				try:
					self.setTracking(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:tracking value as ValueObject."
					traceback.print_exc()
				return
	
				# tracking
			if predicate == PROPERTY.SEAS_COURSE:
				try:
					self.setCourse(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:course value as ValueObject."
					traceback.print_exc()
				return
			
			# pass on to Object
			super(Direction, self).parse(statement)
	