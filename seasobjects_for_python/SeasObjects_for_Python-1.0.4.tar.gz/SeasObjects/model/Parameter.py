from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.Tools import Tools
from SeasObjects.model.Obj import Obj
from SeasObjects.model.Variant import Variant

from SeasObjects.rdf.Resource import Resource
from SeasObjects.rdf.RdfList import RdfList
from SeasObjects.rdf.types import *
from rdflib import Literal

import traceback

class Parameter(Obj):

	def __init__(self, key = None, value = None):
		Obj.__init__(self)
		self.setType(RESOURCE.SEAS_PARAMETER)
		self.key = key
		self.value = value
		
	def hasKey(self):
		return self.key is not None
	
	def setKey(self, k):
		self.key = k
	
	def getKey(self):
		return self.key
	
	def hasValue(self):
		return self.value is not None
	
	def setValue(self, v):
		self.value = v
	
	def getValue(self):
		return self.value
	
	def serialize(self, model):
		resource = super(Parameter, self).serialize(model)
	
		if self.hasKey():
			resource.addProperty(model.createProperty( PROPERTY.SEAS_PARAMETER_KEY ), Literal(self.getKey()))
		
		if self.hasValue():
			if isinstance(self.getValue(), Obj) or isinstance(self.getValue(), Variant):
				resource.addProperty(model.createProperty( PROPERTY.RDF_VALUE ), self.getValue().serialize(model))
			elif isinstance(self.getValue(), list):
				rdfList = model.createList()
				rdfList.add_items(self.getValue())
				resource.addProperty(model.createProperty(PROPERTY.RDF_VALUE), rdfList)
			else:
				resource.addProperty(model.createProperty(PROPERTY.RDF_VALUE), Literal(self.getValue()))
		return resource


	def parse(self, resource, target_class = None):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				para = Parameter(resource.toString())
			else:
				para = Parameter()
			para.clearTypes()
			
			for statement in resource.findProperties():
				# parse statement
				para.parse(statement)
			
			return para
		
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
			
			if predicate == PROPERTY.SEAS_PARAMETER_KEY:
				
				try:
					self.setKey(statement.getString())
				except:
					print "Unable to interpret seas:key value as literal for Parameter."
					traceback.print_exc()
				return
			
			if predicate == PROPERTY.RDF_VALUE:
				target_class = Tools().getResourceClass(statement.getResource())

				if target_class is not None:
					try:
						self.setValue(target_class().parse(statement.getResource()))
					except:
						print "Unable to interpret seas:value as value for Parameter."
						traceback.print_exc()
					return
				elif statement.getResource().model.is_list(statement.getObject()):
					l = []
					statement.getResource().model.parse_list(l, statement.getObject())
					self.setValue(l)
				else:
					self.setValue(Variant().parse(statement))
				return
			
			# pass on to Object
			super(Parameter, self).parse(statement)

