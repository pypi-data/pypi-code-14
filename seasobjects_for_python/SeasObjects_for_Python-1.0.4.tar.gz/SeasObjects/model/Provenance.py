from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.Tools import Tools
from SeasObjects.model.Activity import Activity
from SeasObjects.model.Obj import Obj

from SeasObjects.rdf.Resource import Resource
from SeasObjects.rdf.types import *
from rdflib import XSD

class Provenance(Obj):

	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.generatedBy = None
		self.generatedAt = None
		self.generationMethods = []
		self.dataSources = []
		self.props =[]
		self.setType(RESOURCE.SEAS_PROVENANCE)
		
	def hasGeneratedBy(self):
		return self.generatedBy is not None
	
	def getGeneratedBy(self):
		return self.generatedBy
	
	def setGeneratedBy(self, _generatedBy):
		self.generatedBy = _generatedBy
		
	def hasGeneratedAt(self):
		return True
	
	def getGeneratedAt(self):
		return self.generatedAt
		
	def setGeneratedAt(self, _generatedAt):
		self.generatedAt = _generatedAt
		
	def hasGenerationMethod(self):
		return len(self.generationMethods) > 0
	
	def getGenerationMethods(self):
		return self.generationMethods
	
	def addGenerationMethod(self, generationMethod):
		if isinstance(generationMethod, Obj):
			self.generationMethods.append(generationMethod)
		else:
			self.generationMethods.append(Obj(generationMethod))
	
	def setGenerationMethods(self, _generationMethods):
		self.generationMethods = _generationMethods
		
	def hasDataSource(self):
		return len(self.dataSources) > 0
	
	def getDataSources(self):
		return self.dataSources
	
	def addDataSource(self, dataSource):
		if isinstance(dataSource, Obj):
			self.dataSources.append(dataSource)
		else:
			self.dataSources.append(Obj(dataSource))
			
	def setDataSources(self, _dataSources):
		self.dataSources = dataSources
		
	def hasProperty(self):
		return len(props) > 0
	
	def getProperties(self):
		return self.props
	
	def addProperty(self, property):
		self.props.append(property)
		
	def setProperties(self, _properties):
		self.props = _properties
	
	def serialize(self, model):
		resource = super(Provenance, self).serialize(model)
	
		# generatedby
		if self.hasGeneratedBy():
			resource.addProperty( model.createProperty( PROPERTY.SEAS_GENERATEDBY ), self.generatedBy.serialize(model) )

		# generatedat
		if self.hasGeneratedAt():
			resource.addProperty(model.createProperty( PROPERTY.SEAS_GENERATEDAT ), model.createLiteral(self.getGeneratedAt()))
	
		# generationMethods
		for i in range(len(self.generationMethods)):
			resource.addProperty(model.createProperty( PROPERTY.SEAS_GENERATIONMETHOD ), self.generationMethods[i].serialize(model))
	
		# dataSources
		for i in range(len(self.dataSources)):
			resource.addProperty(model.createProperty( PROPERTY.SEAS_DATASOURCE ), self.dataSources[i].serialize(model))
	
		# props
		for i in range(len(self.props)):
			resource.addProperty( model.createProperty( PROPERTY.SEAS_PROPERTY ), model.createResource( self.props[i]))
	
		return resource


	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				provenance = Provenance(resource.toString())
			else:
				provenance = Provenance()
			provenance.clearTypes()
			
			for statement in resource.findProperties():
				# parse statement
				provenance.parse(statement);
			
			return provenance
		
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
	
			# generatedby
			if predicate == PROPERTY.SEAS_GENERATEDBY:
				try:
					self.setGeneratedBy(Activity().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:generatedBy value as resource."
					traceback.print_exc()
				return
		
			# generatedat
			if predicate == PROPERTY.SEAS_GENERATEDAT:
				try:
					self.setGeneratedAt(statement.getObject().toPython())
				except:
					print "Unable to interpret seas:generatedAt value as date literal."
					traceback.print_exc()
				return
		
			# generationMethod
			if predicate == PROPERTY.SEAS_GENERATIONMETHOD:
				try:
					self.addGenerationMethod(Obj().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:generationMethod value as resource."
					traceback.print_exc()
				return
		
			# dataSource
			if predicate == PROPERTY.SEAS_DATASOURCE:
				try:
					self.addDataSource(Obj().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:dataSource value as resource."
					traceback.print_exc()
				return
		
			# property
			if predicate == PROPERTY.SEAS_PROPERTY:
				try:
					self.addProperty(statement.getResource().toString())
				except:
					print "Unable to interpret seas:property value as resource."
					traceback.print_exc()
				return
		
			# pass on to Obj
			super(Provenance, self).parse(statement)

