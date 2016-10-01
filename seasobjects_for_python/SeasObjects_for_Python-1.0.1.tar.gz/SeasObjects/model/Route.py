from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.CLASS import CLASS
from SeasObjects.rdf.Resource import Resource
from SeasObjects.model.Obj import Obj
from SeasObjects.model.Coordinates import Coordinates


class Route(Obj):
	
	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.setType(CLASS.SEAS_ROUTE)
		self.route_points = []
		
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

		return route
	
	def parse(self, resource):
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

			# interfaceaddress
			if predicate == PROPERTY.SEAS_LIST:
				try:
					self.setRoutePoints(statement.getResource().toList(Coordinates))
				except:
					print "Unable to interpret seas:list value as a resource for Route."
					traceback.print_exc() 
				return
			
			# pass on to Object
			super(Route, self).parse(statement)

