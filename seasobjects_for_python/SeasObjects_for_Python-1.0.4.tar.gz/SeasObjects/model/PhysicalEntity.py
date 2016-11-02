from SeasObjects.model.Entity import Entity
from SeasObjects.rdf.Resource import Resource
from SeasObjects.seasexceptions.NonePointerException import NonePointerException
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from rdflib import XSD

import traceback

class PhysicalEntity(Entity):

	def __init__(self, uri = None):
		Entity.__init__(self, uri)
		self.velocity = None
		self.orientation = None
		self.direction = None
		self.size = None
		self.weight = None
		self.setType(RESOURCE.SEAS_PHYSICALENTITY)
		
	def hasVelocity(self):
		return self.velocity is not None
	
	def getVelocity(self):
		return self.velocity
	
	def setVelocity(self, s):
		self.velocity = s

	def hasOrientation(self):
		return self.orientation is not None
	
	def getOrientation(self):
		return self.orientation
	
	def setOrientation(self, o):
		self.orientation = o

	def hasSize(self):
		return self.size is not None
	
	def getSize(self):
		return self.size
	
	def setSize(self, s):
		self.size = s;

	def hasDirection(self):
		return self.direction is not None
	
	def getDirection(self):
		return self.direction
	
	def setDirection(self, b):
		self.direction = b

	def hasWeight(self):
		return self.weight is not None
	
	def getWeight(self):
		return self.weight;
	
	def setWeight(self, w):
		self.weight = w
	
	
	def serialize(self, model):
		resource = super(PhysicalEntity, self).serialize(model)
	
		# velocity
		if self.hasVelocity():
			resource.addProperty( model.createProperty( PROPERTY.SEAS_SPEED ), self.velocity.serialize(model) )
	
		# orientation
		if self.hasOrientation():
			resource.addProperty( model.createProperty( PROPERTY.SEAS_ORIENTATION ), self.orientation.serialize(model) )
	
		# size
		if self.hasSize():
			resource.addProperty( model.createProperty( PROPERTY.SEAS_SIZE ), self.size.serialize(model) )
	
		# direction
		if self.hasDirection():
			resource.addProperty( model.createProperty( PROPERTY.SEAS_DIRECTION ), self.direction.serialize(model) )
	
		# weight
		if self.hasWeight():
			resource.addProperty( model.createProperty( PROPERTY.SEAS_WEIGHT ), self.weight.serialize(model) )

		return resource
	
	def parse(self, resource):
		from SeasObjects.model.Size import Size
		from SeasObjects.model.Orientation import Orientation
		from SeasObjects.model.Direction import Direction
		from SeasObjects.model.Velocity import Velocity
		from SeasObjects.model.ValueObject import ValueObject
		
		if isinstance(resource, Resource):
			if resource == None:
				raise NullPointerException("Unable to parse null to PhysicalEntity.")
	
			if not resource.isAnon():
				entity = PhysicalEntity(resource.toString())
			else:
				entity = PhysicalEntity()
			entity.clearTypes()
	
			for statement in resource.findProperties():
				# parse statement
				entity.parse(statement)
	
			return entity
		
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())

			# status
			if predicate == PROPERTY.SEAS_SPEED:
				try:
					self.setVelocity(Velocity().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:velocity value as resource."
					traceback.print_exc() 
				return

			# status
			if predicate == PROPERTY.SEAS_ORIENTATION:
				try:
					self.setOrientation(Orientation().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:orientation value."
					traceback.print_exc() 
				return
			
			# status
			if predicate == PROPERTY.SEAS_SIZE:
				try:
					self.setSize(Size().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:size value as resource."
					traceback.print_exc() 
				return
			
			# errors
			if predicate == PROPERTY.SEAS_DIRECTION:
				try:
					self.setDirection(Direction().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:direction value as resource."
					traceback.print_exc() 
				return
			
			if predicate == PROPERTY.SEAS_WEIGHT:
				try:
					self.setWeight(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:weight value as resource."
					traceback.print_exc() 
				return
	
			# pass on to Evaluation
			super(PhysicalEntity, self).parse(statement);