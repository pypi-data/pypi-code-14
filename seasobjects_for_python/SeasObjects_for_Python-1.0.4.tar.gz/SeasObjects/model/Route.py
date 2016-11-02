from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.rdf.Resource import Resource
from SeasObjects.model.Obj import Obj
from SeasObjects.model.Coordinates import Coordinates


class Route(Obj):
	
	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.setType(RESOURCE.SEAS_ROUTE)
		self.route_points = []
		self.length = None
		self.energyConsumption = None
		self.averageVelocity = None
		self.duration = None
	
	def hasRoutePoints(self):
		return len(self.route_points) > 0
	
	def getRoutePoints(self):
		return self.route_points
	
	def setRoutePoints(self, points):
		self.route_points = points
	
	def addRoutePoint(self, point):
		self.route_points.append(point);
	
	def serialize(self, model):
		route = super(Route, self).serialize(model)
		
		if self.hasRoutePoints():
			rdfList = model.createList()
			rdfList.add_items(self.route_points)
			
			route.addProperty(model.createProperty( PROPERTY.SEAS_LIST ), rdfList)

		if self.hasLength():
			route.addProperty(model.createProperty( PROPERTY.SEAS_LENGTH ), self.length.serialize(model));
		
		if self.hasEnergyConsumption():
			route.addProperty(model.createProperty( PROPERTY.SEAS_ENERGYCONSUMPTION ), self.energyConsumption.serialize(model));
		
		if self.hasAverageVelocity():
			route.addProperty(model.createProperty( PROPERTY.SEAS_AVERAGESPEED ), self.averageVelocity.serialize(model));
		
		if self.hasDuration():
			route.addProperty(model.createProperty( PROPERTY.SEAS_DURATION ), self.duration.serialize(model));
		
		return route
	
	def parse(self, resource):
		from SeasObjects.model.Velocity import Velocity
		from SeasObjects.model.ValueObject import ValueObject
		from SeasObjects.model.TemporalContext import TemporalContext
		
		if isinstance(resource, Resource):
			if not resource.isAnon():
				route = Route(resource.toString())
			else:
				route = Route()
			route.clearTypes()

			for statement in resource.findProperties():
				# parse statement
				route.parse(statement)
	
			return route
		
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())

			# route points
			if predicate == PROPERTY.SEAS_LIST:
				try:
					self.setRoutePoints(statement.getResource().toList(Coordinates))
				except:
					print "Unable to interpret seas:list value as a resource for Route."
					traceback.print_exc() 
				return
			
			
			if predicate == PROPERTY.SEAS_LENGTH:
				try:
					self.setLength(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:length value as a resource for Route."
					traceback.print_exc() 
				return
			
			if predicate == PROPERTY.SEAS_ENERGYCONSUMPTION:
				try:
					self.setEnergyConsumption(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:energyconsumption value as a resource for Route."
					traceback.print_exc() 
				return

			if predicate == PROPERTY.SEAS_AVERAGESPEED:
				try:
					self.setAverageVelocity(Velocity().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:averagesoeed value as a resource for Route."
					traceback.print_exc() 
				return

			if predicate == PROPERTY.SEAS_DURATION:
				try:
					self.setDuration(TemporalContext().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:duration value as a resource for Route."
					traceback.print_exc() 
				return
		
			# pass on to Object
			super(Route, self).parse(statement)


	def hasLength(self):
		return self.length is not None
	
	def getLength(self):
		return self.length
	
	def setLength(self, l):
		self.length = l

	def hasEnergyConsumption(self):
		return self.energyConsumption is not None
	
	def getEnergyConsumption(self):
		return self.energyConsumption
	
	def setEnergyConsumption(self, l):
		self.energyConsumption = l

	def hasAverageVelocity(self):
		return self.averageVelocity is not None
	
	def getAverageVelocity(self):
		return self.averageVelocity
	
	def setAverageVelocity(self, l):
		self.averageVelocity = l
		
	def hasDuration(self):
		return self.duration is not None
	
	def getDuration(self):
		return self.duration
	
	def setDuration(self, l):
		self.duration = l
		