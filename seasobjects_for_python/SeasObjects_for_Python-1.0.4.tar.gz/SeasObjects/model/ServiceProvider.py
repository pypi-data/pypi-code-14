from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.model.AbstractEntity import AbstractEntity
from SeasObjects.rdf.Resource import Resource

class ServiceProvider(AbstractEntity):

	def __init__(self, uri = None):
		AbstractEntity.__init__(self, uri)
		self.services = []
		self.setType(RESOURCE.SEAS_SERVICEPROVIDER)

	def setService(self, service):
		self.services = [service]
	
	def addService(self, service):
		self.services.append(service)

	def getServices(self):
		return self.services

	def serialize(self, model):
		entity = super(ServiceProvider, self).serialize(model);
		
		# set services
		offersService = model.createProperty( PROPERTY.SEAS_OFFERSSERVICE )
		for service in services:
			entity.addProperty( offersService, service.serialize(model) )
		
		return entity
	
	def parse(self, resource):
		from SeasObjects.model.Service import Service
		
		if isinstance(resource, Resource):
			if not resource.isAnon():
				serviceProvider = ServiceProvider(resource.toString())
			else:
				serviceProvider = ServiceProvider()
			serviceProvider.clearTypes()
	
			for statement in resource.findProperties():
				# parse statement
				serviceProvider.parse(statement);
	
			return serviceProvider
		
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
	
			# offersservice
			if predicate == PROPERTY.SEAS_OFFERSSERVICE:
				try:
					self.addService(Service().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:offersService value as resource."
					traceback.print_exc() 
				
				return
	
			# pass on to Object
			super(ServiceProvider, self).parse(statement)
