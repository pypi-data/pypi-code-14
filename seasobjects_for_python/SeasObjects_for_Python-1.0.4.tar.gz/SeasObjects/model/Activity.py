from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.rdf.Resource import Resource

from SeasObjects.model.Obj import Obj
from SeasObjects.model.Input import Input

import traceback


class Activity(Obj):

	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.setType(RESOURCE.SEAS_ACTIVITY)
		self.inputs = []
		self.outputs = []
		self.availabilities = []
		self.dataAvailabilities = []
		self.interfaces = []

	def serialize(self, model):
		activity = super(Activity, self).serialize(model)
		# inputs
		for input in self.inputs:
			if input.getInputType() == Input.TYPE_DATA:
				activity.addProperty(model.createProperty( PROPERTY.SEAS_HASINPUT ), input.serialize(model))
			if input.getInputType() == Input.TYPE_REFERENCE:
				activity.addProperty(model.createProperty( PROPERTY.SEAS_HASREFINPUT ), input.serialize(model))	

		# outputs
		for output in self.outputs:
			activity.addProperty(model.createProperty( PROPERTY.SEAS_HASOUTPUT ), output.serialize(model))
	
		# availability
		availabilityProp = model.createProperty( PROPERTY.SEAS_HASAVAILABILITY )
		for availability in self.availabilities:
			activity.addProperty( availabilityProp, availability.serialize(model) )

		# data availability
		dataAvailabilityProp = model.createProperty( PROPERTY.SEAS_HASDATAAVAILABILITY )
		for availability in self.dataAvailabilities:
			activity.addProperty( dataAvailabilityProp, availability.serialize(model) )

		# set interfaces
		for iAddrs in self.interfaces:
			activity.addProperty(model.createProperty( PROPERTY.SEAS_INTERFACE ), iAddrs.serialize(model))

		return activity
	

	def parse(self, resource):
		from SeasObjects.model.Availability import Availability
		from SeasObjects.model.Input import Input
		from SeasObjects.model.Output import Output
		from SeasObjects.model.InterfaceAddress import InterfaceAddress
		
		if isinstance(resource, Resource):
			if not resource.isAnon():
				activity = Activity(resource.toString())
			else:
				activity = Activity()
			activity.clearTypes()
	
			for statement in resource.findProperties():
				# parse statement
				activity.parse(statement);
	
			return activity
		
		else:
			statement = resource
			predicate = str(statement.getPredicate())

			# input data
			if predicate == PROPERTY.SEAS_HASINPUT:
				try:
					self.addInput(Input().parse(statement.getResource()));
				except:
					print "Unable to interpret seas:hasInput value as resource."
					traceback.print_exc()
				return

			# input reference
			if predicate == PROPERTY.SEAS_HASREFINPUT:
				try:
					input = Input().parse(statement.getResource())
					input.setInputType(Input.TYPE_REFERENCE)
					self.addInput(input)
				except:
					print "Unable to interpret seas:hasRefInput value as resource."
					traceback.print_exc()
				return

			# output
			if  predicate == PROPERTY.SEAS_HASOUTPUT:
				try:
					self.addOutput(Output().parse(statement.getResource()));
				except:
					print "Unable to interpret seas:hasOutput value as resource."
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

			# interfaceaddress
			if predicate == PROPERTY.SEAS_INTERFACE:
				try:
					self.addInterface(InterfaceAddress().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:interface value as resource."
					traceback.print_exc()
				return

			# pass on to Object
			super(Activity, self).parse(statement)


	def hasInput(self):
		return len(self.inputs) > 0

	def getInputs(self):
		return self.inputs
	
	def setInput(self, input):
		self.inputs = [input]

	def addInput(self, input):
		self.inputs.append(input)

	def hasOutput(self):
		return len(self.outputs) > 0

	def getOutputs(self):
		return self.outputs
	
	def setOutput(self, output):
		self.outputs = [output]

	def addOutput(self, output):
		self.outputs.append(output)

	def hasAvailability(self):
		return len(self.availabilities) > 0
	
	def getAvailabilities(self):
		return self.availabilities
	
	def addAvailability(self, availability):
		self.availabilities.append(availability)

	def hasDataAvailability(self):
		return len(self.dataAvailabilities) > 0
	
	def getDataAvailabilities(self):
		return self.dataAvailabilities
	
	def addDataAvailability(self, availability):
		self.dataAvailabilities.append(availability)

	def getInterfaces(self):
		return self.interfaces;
	
	def setInterface(self, interfaceAddress):
		self.interfaces = [interfaceAddress]

	def addInterface(self, interfaceAddress):
		self.interfaces.append(interfaceAddress)
