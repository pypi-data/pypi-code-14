from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.rdf.Resource import Resource
from SeasObjects.model.Obj import Obj
from SeasObjects.model.ValueObject import ValueObject

from rdflib import XSD
import traceback

class Size(Obj):
	
	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.height = None
		self.width = None
		self.depth = None
		self.setType(RESOURCE.SEAS_SIZE);
	
	def hasHeight(self):
		return self.height is not None
	
	def setHeight(self, l):
		self.height = l
	
	def getHeight(self):
		return self.height
	
	def hasWidth(self):
		return self.width is not None
	
	def setWidth(self, l):
		self.width = l
	
	def getWidth(self):
		return self.width
	
	def hasDepth(self):
		return self.depth is not None
	
	def setDepth(self, a):
		self.depth = a
	
	def getDepth(self):
		return self.depth
		
	def serialize(self, model):
		size = super(Size, self).serialize(model)
		
		if self.hasWidth():
			size.addProperty(model.createProperty( PROPERTY.SEAS_WIDTH ), self.getWidth().serialize(model))

		if self.hasHeight():
			size.addProperty(model.createProperty( PROPERTY.SEAS_HEIGHT ), self.getHeight().serialize(model))

		if self.hasDepth():
			size.addProperty(model.createProperty( PROPERTY.SEAS_DEPTH ), self.getDepth().serialize(model))

		return size
	
	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				size = Size(resource.toString())
			else:
				size = Size()
			size.clearTypes()
			
			for statement in resource.findProperties():
				# parse statement
				size.parse(statement);
			
			return size
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
	
			# width
			if predicate == PROPERTY.SEAS_WIDTH:
				try:
					self.setWidth(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:width value as literal double."
					traceback.print_exc()
				return
	
			# height
			if predicate == PROPERTY.SEAS_HEIGHT:
				try:
					self.setHeight(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:height value as literal double."
					traceback.print_exc()
				return
			
			# depth
			if predicate == PROPERTY.SEAS_DEPTH:
				try:
					self.setDepth(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:depth value as literal double."
					traceback.print_exc()
				return
				
			# pass on to Object
			super(Size, self).parse(statement)
	