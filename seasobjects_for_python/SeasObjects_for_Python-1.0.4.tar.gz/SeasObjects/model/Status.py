from SeasObjects.model.Obj import Obj
from SeasObjects.model.Variant import Variant
from SeasObjects.model.TemporalContext import TemporalContext

from SeasObjects.rdf.Resource import Resource
from SeasObjects.rdf.Statement import Statement
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from rdflib import XSD

class Status(Obj):
		
	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.setType(RESOURCE.SEAS_STATUS);
		self.percentage = None
		self.total = None
		self.completed = None
		self.temporalContext = None
	
	def serialize(self, model):
		resource = super(Status, self).serialize(model)
		
		# percentage
		if self.hasPercentage():
			resource.addProperty(model.createProperty(PROPERTY.SEAS_PERCENTAGE), self.percentage.serialize(model))

		# total
		if self.hasTotal():
			resource.addProperty(model.createProperty(PROPERTY.SEAS_TOTAL), model.createTypedLiteral(self.total, XSD.int))
	
		# completed
		if self.hasCompleted():
			resource.addProperty(model.createProperty(PROPERTY.SEAS_COMPLETED), model.createTypedLiteral(self.completed, XSD.int))

		# temporalcontext
		if self.hasTemporalContext():
			resource.addProperty(model.createProperty(PROPERTY.SEAS_TEMPORALCONTEXT), self.temporalContext.serialize(model))

		return resource

	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				status = Status(resource.toString())
			else:
				status = Status()
			status.clearTypes()
			
			for i in resource.findProperties():
				# pass on to Evaluation
				status.parse(i)
			
			return status
		else:
			statement = resource
			predicate = str(statement.getPredicate())
	
			# percentage
			if predicate == PROPERTY.SEAS_PERCENTAGE:
				self.setPercentage(Variant().parse(statement))
				return

			# total
			if predicate == PROPERTY.SEAS_TOTAL:
				self.setTotal(statement.getInt())
				return

			# completed
			if predicate == PROPERTY.SEAS_COMPLETED:
				self.setCompleted(statement.getInt())
				return

			# temporalcontext
			if predicate == PROPERTY.SEAS_TEMPORALCONTEXT:
				self.setTemporalContext(TemporalContext().parse(statement.getResource()))
				return

			# pass on to Obj
			super(Status, self).parse(resource)

	
	def setPercentage(self, p):
		if not isinstance(p, Variant):
			self.percentage = Variant(p)
		else:
			self.percentage = p
			
	def setTotal(self, t):
		self.total = t
	
	def setCompleted(self, c):
		self.completed = c
	
	def setTemporalContext(self, t):
		self.temporalContext = t
	
	def getPercentage(self):
		return self.percentage
	
	def getTotal(self):
		return self.total
	
	def getCompleted(self):
		return self.completed
	
	def getTemporalContext(self):
		return self.temporalContext
		
	def hasPercentage(self):
		return self.percentage is not None
	
	def hasTotal(self):
		return self.total is not None
	
	def hasCompleted(self):
		return self.completed is not None
	
	def hasTemporalContext(self):
		return self.temporalContext is not None

	def getPercentageAsInteger():
		return int(self.percentage)

	def getPercentageAsDouble():
		return double(self.percentage)
