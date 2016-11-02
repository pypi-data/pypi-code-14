from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.Tools import Tools
from SeasObjects.model.Obj import Obj
from SeasObjects.model.Variant import Variant

from SeasObjects.rdf.Resource import Resource
from SeasObjects.rdf.RdfList import RdfList
from SeasObjects.rdf.types import *
from rdflib import Literal

class Map(Obj):

	def __init__(self):
		Obj.__init__(self)
		self.setType(RESOURCE.SEAS_MAP)
		self.map = {}
		
	def isEmpty(self):
		return len(self.map.keys()) == 0
	
	def size(self):
		return len(self.map.keys())
	
	def containsKey(self, key):
		return self.map.has_key(key)
	
	def containsValue(self, value):
		# FIXME
		return False

	def get(self, key):
		return self.map[key]
	
	def put(self, key, value):
		self.map[key] = value
		
	def insert(self, key, value):
		self.put(key, value)
	
	def serialize(self, model):
		resource = super(Map, self).serialize(model)
	
		keys = self.map.keys()
		for key in keys:
			entryResource = model.createResource()
			if isinstance(key, Obj):
				entryResource.addProperty(model.createProperty(PROPERTY.SEAS_KEY), key.serialize(model))
			else:
				entryResource.addProperty(model.createProperty(PROPERTY.SEAS_KEY), Literal(key))
			
			if isinstance(self.map[key], Obj) or isinstance(self.map[key], Variant):
				entryResource.addProperty(model.createProperty( PROPERTY.RDF_VALUE ), self.map[key].serialize(model))
			elif isinstance(self.map[key], list):
				rdfList = model.createList()
				rdfList.add_items(self.map[key])
				entryResource.addProperty(model.createProperty(PROPERTY.RDF_VALUE), rdfList)
			else:
				entryResource.addProperty(model.createProperty(PROPERTY.RDF_VALUE), Literal(self.map[key]))
			
			resource.addProperty(model.createProperty(PROPERTY.SEAS_ENTRY), entryResource)

		return resource


	def parse(self, resource):
		from SeasObjects.model.Variant import Variant
		
		if isinstance(resource, Resource):
			if not resource.isAnon():
				map = Map(resource.toString())
			else:
				map = Map()
			map.clearTypes()
			
			for statement in resource.findProperties():
				# parse statement
				map.parse(statement);
			
			return map
		
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
			# entry
			if predicate == PROPERTY.SEAS_ENTRY:
				entry = statement.getResource()
				keyStmt = entry.findProperty(entry.getModel().createProperty(PROPERTY.SEAS_KEY))
				valueStmt = entry.findProperty(entry.getModel().createProperty(PROPERTY.RDF_VALUE))
				
				if keyStmt and valueStmt and len(keyStmt) > 0 and len(valueStmt) > 0:
					key = Variant().parse(keyStmt[0])
					s = valueStmt[0]
					
					target_class = Tools().getResourceClass(s.getResource())
					if target_class is not None:
						try:
							value = target_class().parse(s.getResource())
						except:
							print "Unable to interpret seas:value as value for Parameter."
							traceback.print_exc()
							return
					else:
						value = Variant().parse(s)
					
					if key != None and value != None:
						self.map[key.getValue()] = value
					else:
						print "Null key or value found in map entry while parsing. Entry dropped.";
				else:
					print "Null key or value found in map entry while parsing. Entry dropped.";
					
				return

			# pass on to Object
			super(Map, self).parse(statement)

