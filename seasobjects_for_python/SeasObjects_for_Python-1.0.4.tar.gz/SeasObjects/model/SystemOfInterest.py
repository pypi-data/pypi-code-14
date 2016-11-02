from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.model.Entity import Entity
from SeasObjects.model.Evaluation import Evaluation
from SeasObjects.rdf.Resource import Resource

import sys
import traceback

class SystemOfInterest(Entity):

	def __init__(self, uri = None):
		Entity.__init__(self, uri)
		self.registerKey = None
		self.realizedBy = None
		self.setType(RESOURCE.SEAS_SYSTEM_OF_INTEREST)
	
	def serialize(self, model):
		systemOfInterest = super(SystemOfInterest, self).serialize(model)
		
		# registerkey
		if self.hasRegisterKey():
			systemOfInterest.addProperty(model.createProperty( PROPERTY.SEAS_REGISTERKEY ), self.registerKey)

		if self.isRealizedBy():
			systemOfInterest.addProperty(model.createProperty( PROPERTY.SEAS_REALIZEDBY ), self.realizedBy.serialize(model) )

		return systemOfInterest

	def parse(self, resource):
		from SeasObjects.model.PhysicalEntity import PhysicalEntity
		
		if isinstance(resource, Resource):
			if not resource.isAnon():
				systemOfInterest = SystemOfInterest(resource.toString())
			else:
				systemOfInterest = SystemOfInterest()
			systemOfInterest.clearTypes()
	
			for statement in resource.findProperties():
				systemOfInterest.parse(statement)
			
			return systemOfInterest
		
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
				
			# reg key
			if predicate == PROPERTY.SEAS_REGISTERKEY:
				try:
					self.setRegisterKey(statement.getString())
				except:
					print "Unable to interpret seas:registerKey value as literal string."
					print sys.exc_info()[1]
					traceback.print_exc() 
				return
			
			# reg key
			if predicate == PROPERTY.SEAS_REALIZEDBY:
				try:
					self.setRealizedBy(PhysicalEntity().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:realizedBy value as resource."
					print sys.exc_info()[1]
					traceback.print_exc() 
				return

			# pass on to Object
			super(SystemOfInterest, self).parse(statement)
		
	def hasRegisterKey(self):
		return self.registerKey is not None

	def getRegisterKey(self):
		return self.registerKey
	
	def setRegisterKey(self, registerKey):
		self.registerKey = registerKey

	def isRealizedBy(self):
		return self.realizedBy is not None

	def getRealizedBy(self):
		return self.realizedBy
	
	def setRealizedBy(self, rb):
		self.realizedBy = rb
