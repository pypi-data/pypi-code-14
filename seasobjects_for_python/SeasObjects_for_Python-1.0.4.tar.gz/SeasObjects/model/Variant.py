from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.VARIANT import VARIANT
from SeasObjects.model.Obj import Obj
from SeasObjects.rdf.Resource import Resource
from SeasObjects.common.Tools import Tools

from rdflib import Literal, BNode, URIRef

import datetime

class Variant(object):

	def __init__(self, value = None):
		self.variant = value
	
	def serialize(self, model):
		if self.isObj():
			return self.variant.serialize(model)
		else:
			return self.asTerm()

	def asTerm(self):
		if self.isUri():
			return self.variant
		elif self.isNull():
			return None
		else:
			return Literal(self.variant)

	def parse(self, statement):
		# get predicate and object
		predicate = str(statement.getPredicate())
		objectNode = statement.getObject()

		# if literal object
		dataType = None
		if isinstance(objectNode, Literal):
			return Variant(objectNode.toPython())
		
		elif isinstance(objectNode, BNode):
			l = []
			statement.getResource().getModel().parse_list(l, objectNode, None)
			return l
		
		elif isinstance(objectNode, URIRef):
			return Variant(objectNode)
		
		# if resource
		elif isinstance(objectNode, Resource):
			resource = statement.getResource()
			klass = Tools().getResourceClass(resource, default = Obj)

			if klass is not None:
				self.add(URIRef(predicate), Variant(klass().parse(resource)))
			else:
				# None found, resort to Obj (the base class)
				self.add(URIRef(predicate), Variant(Obj().parse(resource)))
			
			return

		# could not identify datatype
		print "Parsing variant failed. Unable to detect RDFDatatype (" + str(dataType) + ") for literal."
		return Variant("");


	def isNull(self):
		return self.variant is None

	def isUri(self):
		return isinstance(self.variant, URIRef)
	
	def isString(self):
		return isinstance(self.variant, string)
	
	def isInteger(self):
		return isinstance(self.variant, int)

	def isDouble(self):
		return isinstance(self.variant, double)
		
	def isFloat(self):
		return isinstance(self.variant, float)

	def isBoolean(self):
		return isinstance(self.variant, boolean)

	def isDate(self):
		return isinstance(self.variant, datetime.date)

	def isTime(self):
		return isinstance(self.variant, datetime.time)
	
	def isDateTime(self):
		return isinstance(self.variant, datetime.datetime)
	
	def isMap(self):
		from SeasObjects.model.Map import Map
		return isinstance(self.variant, Map)
	
	def isObj(self):
		return isinstance(self.variant, Obj)

	def getValue(self):
		if isinstance(self.variant, Literal):
			self.variant.toPython()
		return self.variant

	def getType(self):
		return self.type

	def getAsString(self):
		return str(self.variant)
