from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.model.Obj import Obj
from SeasObjects.model.Evaluation import Evaluation
from SeasObjects.model.SystemOfInterest import SystemOfInterest
from SeasObjects.model.TemporalContext import TemporalContext

import traceback

from rdflib import XSD


class TimeSeries(Obj):

	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.quantity = None
		self.unit = None
		self.timeStep = None
		self.list = []
		self.systemOfInterest = None
		self.temporalContext = None
		self.setType(RESOURCE.SEAS_TIMESERIES)

	def serialize(self, model):
		ts = super(TimeSeries, self).serialize(model);

		# quantity
		if self.hasQuantity():
			quantity = model.createResource(self.quantity)
			ts.addProperty(model.createProperty( PROPERTY.SEAS_QUANTITY ), quantity)
		
		# unit
		if self.hasUnit():
			unit = model.createResource(self.unit)
			ts.addProperty(model.createProperty( PROPERTY.SEAS_UNIT ), unit)

		# timestep
		if self.hasTimeStep():
			ts.addProperty(model.createProperty( PROPERTY.SEAS_TIMESTEP ), model.createTypedLiteral(self.getTimeStep(), XSD.duration))
	
		# list
		if self.hasList():
			rdfList = model.createList()
			rdfList.add_items(self.list)
			
			ts.addProperty(model.createProperty( PROPERTY.SEAS_LIST ), rdfList)

		# systemOfInterest
		if self.hasSystemOfInterest():
			ts.addProperty(model.createProperty( PROPERTY.SEAS_SYSTEMOFINTEREST ), self.systemOfInterest.serialize(model))

		# temporalcontext
		if self.hasTemporalContext():
			ts.addProperty(model.createProperty( PROPERTY.SEAS_TEMPORALCONTEXT ), self.temporalContext.serialize(model))

		return ts;

	def parse(self, resource):
		if not resource.isAnon():
			timeSeries = TimeSeries(resource.toString())
		else:
			timeSeries = TimeSeries()
		timeSeries.clearTypes()

		for statement in resource.findProperties():
			# get predicate
			predicate = str(statement.getPredicate())

			# quantity
			if predicate == PROPERTY.SEAS_QUANTITY:
				try:
					timeSeries.setQuantity(statement.getResource().toString())
				except:
					print "Unable to interpret seas:quantity value as resource."
					traceback.print_exc() 
				continue

			# unit
			if predicate == PROPERTY.SEAS_UNIT:
				try:
					timeSeries.setUnit(statement.getResource().toString())
				except:
					print "Unable to interpret seas:unit value as resource."
					traceback.print_exc() 
				continue

			# timestep
			if predicate == PROPERTY.SEAS_TIMESTEP:
				try:
					timeSeries.setTimeStep(statement.getString());
				except:
					print "Unable to interpret seas:timeStep value as literal string."
					traceback.print_exc() 
				continue

			# list
			if predicate == PROPERTY.SEAS_LIST:
				try:
					timeSeries.setList(statement.getResource().toList(Evaluation))
				except:
					print "Unable to interpret seas:list value as resource."
					traceback.print_exc() 
				continue

			# systemofinterest
			if predicate == PROPERTY.SEAS_SYSTEMOFINTEREST:
				try:
					timeSeries.setSystemOfInterest(SystemOfInterest().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:systemOfInterest value as resource."
					traceback.print_exc() 
				continue

			# temporalcontext
			if predicate == PROPERTY.SEAS_TEMPORALCONTEXT:
				try:
					timeSeries.setTemporalContext(TemporalContext().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:temporalContext value as resource."
					traceback.print_exc() 
				continue

			# pass on to Object
			super(TimeSeries, timeSeries).parse(statement)
		
		return timeSeries


	def hasQuantity(self):
		return self.quantity is not None

	def getQuantity(self):
		return self.quantity
	
	def setQuantity(self, quantity):
		self.quantity = quantity

	def hasUnit(self):
		return self.unit is not None

	def getUnit(self):
		return self.unit
	
	def setUnit(self, unit):
		self.unit = unit

	def hasTimeStep(self):
		return self.timeStep is not None
	
	def getTimeStep(self):
		return self.timeStep
	
	def setTimeStep(self, timeStep):
		self.timeStep = timeStep

	def hasList(self):
		return len(self.list) > 0
	
	def getList(self):
		return self.list

	def setList(self, list):
		self.list = list

	def addListItem(self, evaluation):
		self.list.append(evaluation)

	def hasSystemOfInterest(self):
		return self.systemOfInterest is not None

	def setSystemOfInterest(self):
		return self.systemOfInterest

	def setSystemOfInterest(self, system):
		self.systemOfInterest = system

	def hasTemporalContext(self):
		return self.temporalContext is not None

	def getTemporalContext(self):
		return self.temporalContext

	def setTemporalContext(self, temporalContext):
		self.temporalContext = temporalContext
