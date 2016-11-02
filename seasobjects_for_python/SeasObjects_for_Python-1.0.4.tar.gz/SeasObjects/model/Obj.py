
import datetime
import traceback

from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.Tools import Tools
from SeasObjects.rdf.Resource import Resource
from SeasObjects.rdf.Statement import Statement

from rdflib.term import Literal, BNode
from rdflib import URIRef


class Obj(object):
	def __init__(self, seasIdentifierUri = None):
		self.seasIdentifierUri = seasIdentifierUri
		self.sameAs = None
		self.name = None
		self.description = None
		self.types = []
		self.provenances = []

		# map for properties (name, propertyobject pairs)
		self.properties = {}

	def _convert(self, obj, model):
		if isinstance(obj, Obj):
			return obj.serialize(model)
		elif isinstance(obj, URIRef):
			return obj
		else:
			return Literal(obj)
	
	def serialize(self, model):
		# create resource
		if self.hasSeasIdentifierUri():
			resource = model.createResource( self.seasIdentifierUri )
		else:
			resource = model.createResource()
		
		# sameas
		if self.hasSameAs():
			sameAsRes = model.createResource(self.sameAs)
			owlSameAs = model.createProperty( PROPERTY.OWL_SAMEAS )
			resource.addProperty( owlSameAs, sameAsRes )

		# types
		typeProp = model.createProperty( PROPERTY.RDF_TYPE )
		for type in self.types:
			try:
				serialized = type.serialize(model)
			except:
				serialized = URIRef(type)
			resource.addProperty( typeProp, serialized )

		# provenances
		provenanceProp = model.createProperty( PROPERTY.SEAS_PROVENANCE )
		for p in self.provenances:
			resource.addProperty( provenanceProp, p.serialize(model) )

		# name
		if self.hasName():
			rdfsLabel = model.createProperty( PROPERTY.RDFS_LABEL )
			resource.addProperty( rdfsLabel, self.name )

		# comment
		if self.hasDescription():
			rdfsComment = model.createProperty( PROPERTY.RDFS_COMMENT )
			resource.addProperty( rdfsComment, self.description )

		# add object properties
		for key, entry in self.properties.iteritems():
			if isinstance(entry, list):
				for e in entry:
					self._add_property(resource, key, e, model)
			else:
				self._add_property(resource, key, entry, model)

		return resource;

	def _add_property(self, resource, property, entry, model):
		from SeasObjects.model.Parameter import Parameter
		
		if not isinstance(property, URIRef):
			obj = Parameter(key = property, value = entry)
			property = PROPERTY.SEAS_PARAMETER
		else:
			obj = entry
		resource.addProperty( model.createProperty( property ), self._convert(obj, model))
			
	def parse(self, element):
		from SeasObjects.model.Parameter import Parameter
		from SeasObjects.model.Provenance import Provenance
		
		if isinstance(element, Resource):
			if not element.isAnon():
				obj = Obj(element.toString())
			else:
				obj = Obj()
	
			for i in element.findProperties():
				obj.parse(i)
	
			return obj

		elif isinstance(element, Statement):
			statement = element
	
			# get predicate and object
			predicate = str(statement.getPredicate())
			objectNode = statement.getObject()
			
			# type
			if predicate == PROPERTY.RDF_TYPE:
				try:
					self.addType(URIRef(statement.getResource().toString()))
				except:
					print "Unable to interpret rdf:type value as resource."
					traceback.print_exc()
				return
	
			# sameas
			if predicate == PROPERTY.OWL_SAMEAS:
				try:
					self.setSameAs(statement.getResource().toString())
				except:
					print"Unable to interpret owl:sameAs value as resource."
					traceback.print_exc()
				return

			# provenance
			if predicate == PROPERTY.SEAS_PROVENANCE:
				try:
					self.addProvenance(Provenance().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:provenance value as resource."
					traceback.print_exc() 
				return

			# label
			if predicate == PROPERTY.RDFS_LABEL:
				try:
					self.setName(statement.getString())
				except:
					print"Unable to interpret rdfs:label value as literal string."
					traceback.print_exc()
				return
	
			# comment
			if predicate == PROPERTY.RDFS_COMMENT:
				try:
					self.setDescription(statement.getString())
				except:
					print"Unable to interpret rdfs:comment value as literal string."
					traceback.print_exc()
				return
	
			# parameters
			if predicate == PROPERTY.SEAS_PARAMETER:
				p = Parameter().parse(statement.getResource())
				self.add(p.getKey(), p.getValue())
				return 
			
			# if literal object
			if isinstance(objectNode, Literal):
				self.add(URIRef(predicate), objectNode.toPython())
				return
			
			if isinstance(objectNode, URIRef):
				self.add(URIRef(predicate), objectNode)
				return
				
			if isinstance(objectNode, BNode):
				self.add(URIRef(predicate), objectNode.toPython())
				return
	
			# if resource
			if isinstance(objectNode, Resource):
				resource = statement.getResource()
				
				# first check if resource has a type implemented built-in
				# and parse using that
				klass = Tools().getResourceClass(resource, default = Obj)

				if klass is not None:
					self.add(URIRef(predicate), klass().parse(resource))
				else:
					# None found, resort to Obj (the base class)
					self.add(URIRef(predicate), Obj().parse(resource));
				
				return	
				

	def getId(self):
		return self.toString()
	
	def toString(self):
		return str(self.getSeasIdentifierUri())
	
	def hasSeasIdentifierUri(self):
		# empty string is not allowed
		return (self.seasIdentifierUri is not None and self.seasIdentifierUri != "")

	def setSeasIdentifierUri(self, uri):
		self.seasIdentifierUri = uri

	def getSeasIdentifierUri(self):
		return self.seasIdentifierUri

	def hasSameAs(self):
		# empty string is not allowed
		return (self.sameAs is not None and self.sameAs != "")

	def setSameAs(self, uri):
		self.sameAs = uri

	def getSameAs(self):
		return self.sameAs
	
	def isOfType(self, type):
		if not isinstance(type, URIRef):
			type = URIRef(type)
		return type in self.types
	
	def hasType(self):
		return len(self.types) > 0

	def clearTypes(self):
		self.types = []
		
	def setType(self, type):
		self.types = [type]

	def addType(self, type):
		self.types.append(type)

	def getTypes(self):
		return self.types

	def hasName(self):
		return self.name is not None
	
	def setName(self, name):
		self.name = name
	
	def getName(self):
		return self.name

	def hasDescription(self):
		return self.description is not None
	
	def setDescription(self, description):
		self.description = description
	
	def getDescription(self):
		return self.description

	def hasProvenance(self):
		return len(self.provenances) > 0

	def getProvenances(self):
		return self.provenances

	def addProvenance(self, p):
		self.provenances.append(p)
		
	def listProperties(self):
		return self.getProperties().values()
	
	def hasProperties(self):
		return len(self.properties) > 0
	
	def getProperties(self):
		from Variant import Variant
		map = {}
		
		for key, value in self.properties.iteritems():
			for e in value:
				# if a key does not exist yet, create new entry
				if not map.has_key(key):
					map[key] = []

				# add to arraylist
				map[key].append(Variant(e))

		return map

	def get(self, property):
		from Variant import Variant
		ret = []
		
		if self.properties.has_key(property):
			for e in self.properties[property]:
				if isinstance(e, Variant):
					ret.append(e)
				else:
					ret.append(Variant(e))
		
		return ret

	def add(self, property, obj):
		if not self.properties.has_key(property):
			self.properties[property] = []
		
		self.properties[property].append(obj)

	def remove(self, property, obj):
		if self.properties.has_key(property):
			del self.properties[property]
