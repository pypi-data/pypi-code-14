from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.model.ServiceProvider import ServiceProvider


class WeatherServiceProvider(ServiceProvider):

	def __init__(self, uri = None):
		ServiceProvider.__init__(self)
		self.addType(RESOURCE.SEAS_WEATHERSERVICEPROVIDER);
		self.setSeasIdentifierUri(uri);
		

	def serialize(self, model):
		return super(WeatherServiceProvider, self).serialize(model)
	
	def parse(self, resource):
		if not resource.isAnon():
			weatherServiceProvider = WeatherServiceProvider(resource.toString())
		else:
			weatherServiceProvider = WeatherServiceProvider()
		weatherServiceProvider.clearTypes()
		
		for statement in resource.findProperties():
			# pass on to ServiceProvider
			weatherServiceProvider.parse(statement);
		
		return weatherServiceProvider;
