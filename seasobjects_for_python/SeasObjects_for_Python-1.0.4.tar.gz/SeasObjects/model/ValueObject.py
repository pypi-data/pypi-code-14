from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.model.Obj import Obj
from SeasObjects.model.Variant import Variant

from rdflib import URIRef
import traceback


class ValueObject(Obj):

	def __init__(self, uri = None, quantity = None, unit = None, value = None):
		Obj.__init__(self, uri)
		if quantity is not None and not isinstance(quantity, URIRef): quantity = URIRef(quantity)
		if unit is not None and not isinstance(unit, URIRef): unit = URIRef(unit)
		self.quantity = quantity
		self.unit = unit
		self.value = value
		self.setType(RESOURCE.SEAS_VALUEOBJECT)

	def serialize(self, model):
		valueObject = super(ValueObject, self).serialize(model)

		# quantity
		if self.hasQuantity():
			quantity = model.createResource(self.quantity)
			valueObject.addProperty(model.createProperty( PROPERTY.SEAS_QUANTITY ), self.quantity)
		
		# unit
		if self.hasUnit():
			unit = model.createResource(self.unit)
			valueObject.addProperty(model.createProperty( PROPERTY.SEAS_UNIT ), self.unit)

		# value
		if self.hasValue():
			valueObject.addProperty(model.createProperty( PROPERTY.SEAS_VALUE ), self.value.serialize(model))

		return valueObject
	
	
	def parse(self, resource):
		if not resource.isAnon():
			valueObject = ValueObject(resource.toString())
		else:
			valueObject = ValueObject()
		valueObject.clearTypes()

		for statement in resource.findProperties():
			# get predicate
			predicate = str(statement.getPredicate())

			# quantity
			if predicate == PROPERTY.SEAS_QUANTITY:
				try:
					valueObject.setQuantity(statement.getResource().toString());
				except:
					print "Unable to interpret seas:quantity value as resource."
					traceback.print_exc() 
				continue

			# unit
			if predicate == PROPERTY.SEAS_UNIT:
				try:
					valueObject.setUnit(statement.getResource().toString())
				except:
					print "Unable to interpret seas:unit value as resource."
					traceback.print_exc() 
				continue
			
			# value
			if predicate == PROPERTY.SEAS_VALUE:
				valueObject.setValue(Variant().parse(statement))
				continue

			# pass on to Obj
			super(ValueObject, valueObject).parse(statement)
		
		return valueObject

	def hasQuantity(self):
		return self.quantity is not None

	def getQuantity(self):
		return self.quantity
	
	def setQuantity(self, quantity):
		self.quantity = URIRef(quantity)

	def hasUnit(self):
		return self.unit is not None

	def getUnit(self):
		return self.unit
	
	def setUnit(self, unit):
		self.unit = URIRef(unit)

	def hasValue(self):
		return self.value is not None
	
	def getValue(self):
		return self.value

	def setValue(self, value):
		self.value = value
