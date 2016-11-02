from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.model.Obj import Obj
from SeasObjects.rdf.types import *

from rdflib import XSD


class InterfaceAddress(Obj):

	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.host = None
		self.port = None
		self.path = None
		self.scheme = None
		self.contentTypes = []
		self.setType(RESOURCE.SEAS_INTERFACEADDRESS);
	
	def serialize(self, model):
		interfaceAddress = super(InterfaceAddress, self).serialize(model)
		
		# host
		if self.hasHost():
			interfaceAddress.addProperty(model.createProperty( PROPERTY.SEAS_HOST ), self.host)

		# port
		if self.hasPort():
			interfaceAddress.addProperty(model.createProperty( PROPERTY.SEAS_PORT ), model.createTypedLiteral(self.port, XSD.integer))

		# path
		if self.hasPath():
			interfaceAddress.addProperty(model.createProperty( PROPERTY.SEAS_PATH ), self.path)

		# scheme
		if self.hasScheme():
			interfaceAddress.addProperty(model.createProperty( PROPERTY.SEAS_SCHEME ), self.scheme)

		# content types
		for cType in self.contentTypes:
			interfaceAddress.addProperty(model.createProperty( PROPERTY.SEAS_CONTENTTYPE ), cType)

		return interfaceAddress

	
	def parse(self, resource):
		if not resource.isAnon():
			interfaceAddress = InterfaceAddress(resource.toString())
		else:
			interfaceAddress = InterfaceAddress()
		interfaceAddress.clearTypes()

		for statement in resource.findProperties():
			# get predicate
			predicate = str(statement.getPredicate())

			# scheme
			if predicate == PROPERTY.SEAS_SCHEME:
				try :
					interfaceAddress.scheme = statement.getString();
				except:
					print "Unable to interpret seas:scheme value as literal string."
					traceback.print_exc()
				continue
			
			# host
			if predicate == PROPERTY.SEAS_HOST:
				try :
					interfaceAddress.host = statement.getString();
				except:
					print "Unable to interpret seas:host value as literal string."
					traceback.print_exc()
				continue

			# port
			if predicate == PROPERTY.SEAS_PORT:
				try:
					interfaceAddress.port = statement.getInt();
				except:
					print "Unable to interpret seas:port value as literal integer."
					traceback.print_exc()
				continue

			# path
			if predicate == PROPERTY.SEAS_PATH:
				try:
					interfaceAddress.path = statement.getString()
				except:
					print"Unable to interpret seas:path value as literal string."
					traceback.print_exc()
				continue

			# content-type
			if predicate == PROPERTY.SEAS_CONTENTTYPE:
				try:
					interfaceAddress.addContentType(statement.getString())
				except:
					print"Unable to interpret seas:contentType value as literal string."
					traceback.print_exc()
				continue

			# pass on to Object
			super(InterfaceAddress, interfaceAddress).parse(statement)
		
		return interfaceAddress
	
	
	def hasHost(self):
		return self.host is not None
	
	def setHost(self, host):
		self.host = host
	
	def getHost(self):
		return self.host
	
	def hasPort(self):
		return self.port is not None

	def setPort(self, port):
		self.port = port
	
	def getPort(self):
		return self.port
	
	def hasPath(self):
		return self.path is not None

	def setPath(self, path):
		self.path = path
	
	def getPath(self):
		return self.path
	
	def hasScheme(self):
		return self.scheme != None

	def setScheme(self, scheme):
		self.scheme = scheme
	
	def getScheme(self):
		return self.scheme
	
	def hasContentType(self):
		return len(self.contentTypes) > 0
	
	def setContentType(self, type):
		self.contentTypes = [type]
	
	def addContentType(self, type):
		self.contentTypes.append(type)
	
	def getContentType(self):
		return self.contentTypes
