from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.CLASS import CLASS
from SeasObjects.rdf.Resource import Resource
from SeasObjects.model.Obj import Obj

import sys
import traceback

class Entity(Obj):

	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.url = None
		self.location = None
		self.controllabilities = []
		self.availabilities = []
		self.dataAvailabilities = []
		self.capabilities = []
		self.capacities = []
		self.interfaces = []
		self.setType(CLASS.SEAS_ENTITY)

	
	def serialize(self, model):
		entity = super(Entity, self).serialize(model)
		
		# hasUrl
		if self.hasUrl():
			entity.addProperty( model.createProperty( PROPERTY.VCARD_HASURL ), self.url )

		# location
		if self.hasLocation():
			entity.addProperty(model.createProperty( PROPERTY.SEAS_LOCATION ), self.location.serialize(model))
		
		# controllability
		for controllability in self.controllabilities:
			entity.addProperty( model.createProperty( PROPERTY.SEAS_HASEVALUATION ), controllability.serialize(model) )

		# availability
		for availability in self.availabilities:
			entity.addProperty( model.createProperty( PROPERTY.SEAS_HASAVAILABILITY ), availability.serialize(model) )

		# data availability
		for availability in self.dataAvailabilities:
			entity.addProperty( model.createProperty( PROPERTY.SEAS_HASDATAAVAILABILITY ), availability.serialize(model) )

		# capacities
		for cap in self.capacities:
			entity.addProperty(model.createProperty( PROPERTY.SEAS_CAPACITY ), cap.serialize(model))
		
		# set interfaces
		for iAddrs in self.interfaces:
			service.addProperty(model.createProperty( PROPERTY.SEAS_INTERFACE ), iAddrs.serialize(model))
		
		# capabilites
		hasCapabilityProp = model.createProperty( PROPERTY.SEAS_HASCAPABILITY )
		if self.hasCapability():
			for activity in self.capabilities:
				activityRes = activity.serialize(model)
				entity.addProperty( hasCapabilityProp, activityRes )

		return entity
	
	def parse(self, resource):
		from SeasObjects.model.Location import Location
		from SeasObjects.model.Controllability import Controllability
		from SeasObjects.model.Availability import Availability
		from SeasObjects.model.Activity import Activity
		from SeasObjects.model.Evaluation import Evaluation
		
		if isinstance(resource, Resource):
			if not resource.isAnon():
				entity = Entity(resource.toString())
			else:
				entity = Entity()
			entity.clearTypes()
			
			for i in resource.findProperties():
				# parse statement
				entity.parse(i);
				
			return entity

		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
	
			# hasurl
			if predicate == PROPERTY.VCARD_HASURL:
				try:
					self.setUrl(statement.getString());
				except:
					print "Unable to interpret vcard:hasURL value as string literal."
					print sys.exc_info()[1]
					traceback.print_exc()
	
				return
	
			# location
			if predicate == PROPERTY.SEAS_LOCATION:
				try:
					self.setLocation(Location().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:location value as resource."
					print sys.exc_info()[1]
					traceback.print_exc()
				return
	
			# controllability
			if predicate == PROPERTY.SEAS_HASEVALUATION:
				try:
					self.addControllability(Controllability().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:hasEvaluation value as resource."
					traceback.print_exc()
				return
	
			# availability
			if predicate == PROPERTY.SEAS_HASAVAILABILITY:
				try:
					self.addAvailability(Availability().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:hasAvailability value as resource."
					traceback.print_exc()
				return
	
			# data availability
			if predicate == PROPERTY.SEAS_HASDATAAVAILABILITY:
				try:
					self.addDataAvailability(Availability().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:hasDataAvailability value as resource."
					traceback.print_exc()
				return
	
			# hascapability
			if predicate == PROPERTY.SEAS_HASCAPABILITY:
				try:
					self.addCapability(Activity().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:hasCapability value as resource."
					traceback.print_exc()
				return
			
			# capacity
			if predicate == PROPERTY.SEAS_CAPACITY:
				try:
					self.addCapacity(Evaluation().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:capacity value as resource."
					traceback.print_exc() 
				return
	
				# interfaceaddress
			if predicate == PROPERTY.SEAS_INTERFACE:
				try:
					self.addInterface(InterfaceAddress().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:interface value as resource."
					traceback.print_exc() 

		# pass on to Object
			super(Entity, self).parse(statement)

	
	def hasLocation(self):
		return (self.location is not None)
	
	def getLocation(self):
		return self.location

	def setLocation(self, location):
		self.location = location
	
	def hasUrl(self):
		return self.url != None

	def setUrl(self, url):
		self.url = url
	
	def getUrl(self):
		return self.url

	def hasControllability(self):
		return len(controllabilities) > 0
	
	def getControllabilities(self):
		return self.controllabilities
	
	def addControllability(self, controllability):
		self.controllabilities.append(controllability)

	def hasAvailability(self):
		return len(self.availabilities) > 0
	
	def getAvailabilities(self):
		return self.availabilities
	
	def addAvailability(self, availability):
		self.availabilities.append(availability)

	def hasDataAvailability(self):
		return len(dataAvailabilities) > 0
	
	def getDataAvailabilities(self):
		return self.dataAvailabilities
	
	def addDataAvailability(self, availability):
		self.dataAvailabilities.append(availability)

	def hasCapability(self):
		return len(self.capabilities) > 0

	def setCapabilities(self, capabilities):
		self.capabilities = capabilities

	def addCapability(self, capability):
		self.capabilities.append(capability)

	def getCapabilities(self):
		return self.capabilities

	def hasCapacities(self):
		return len(self.capacities) > 0

	def getCapacities(self):
		return self.capacities
	
	def addCapacity(self, cap):
		self.capacities.append(cap)
	
	def hasInterface(self):
		return len(self.interfaces) > 0
		
	def getInterfaces(self):
		return self.interfaces

	def setInterface(self, interfaceAddress):
		self.interfaces = [interfaceAddress]

	def addInterface(self, interfaceAddress):
		self.interfaces.append(interfaceAddress)

	