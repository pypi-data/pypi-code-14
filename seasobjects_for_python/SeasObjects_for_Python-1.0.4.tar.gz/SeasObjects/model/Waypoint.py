from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.rdf.Resource import Resource
from SeasObjects.model.Obj import Obj
from SeasObjects.model.Location import Location
from SeasObjects.model.Route import Route
from SeasObjects.model.Variant import Variant

import datetime
from dateutil import parser

class Waypoint(Obj):
	
	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.setType(RESOURCE.SEAS_WAYPOINT);
		self.location = None
		self.instant = None
		self.route = None
		
	def hasLocation(self):
		return self.location is not None
	
	def getLocation(self):
		return self.location

	def setLocation(self, location):
		self.location = location

	def hasInstant(self):
		return self.instant is not None
	
	def getInstant(self):
		return self.instant

	def setInstant(self, instant):
		self.instant = Variant(instant)

	def hasRoute(self):
		return self.route is not None
	
	def getRoute(self):
		return self.route
	
	def setRoute(self, route):
		self.route = route
	
		
	def serialize(self, model):
		waypoint = super(Waypoint, self).serialize(model)
			
		if self.hasLocation():
			waypoint.addProperty(model.createProperty( PROPERTY.SEAS_LOCATION ), self.getLocation().serialize(model))
		
		if self.hasInstant():
			waypoint.addProperty(model.createProperty( PROPERTY.SEAS_INSTANT ), model.createLiteral(self.getInstant().getValue()))
		
		if self.hasRoute():
			waypoint.addProperty(model.createProperty( PROPERTY.SEAS_ROUTE ), self.getRoute().serialize(model))
		
		return waypoint
	
	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				waypoint = Waypoint(resource.toString())
			else:
				waypoint = Waypoint()
			waypoint.clearTypes()
	
			for statement in resource.findProperties():
				waypoint.parse(statement)
		
			return waypoint	
		else:
			statement = resource
			predicate = str(statement.getPredicate())

			# location
			if predicate == PROPERTY.SEAS_LOCATION:
				self.setLocation(Location().parse(statement.getResource()))
				return
			
			# instant
			if predicate == PROPERTY.SEAS_INSTANT:
				e = statement.getObject().toPython()
				if not isinstance(e, datetime.datetime):
					e = parser.parse(e)
				self.setInstant(e)
				return
			
			# location
			if predicate == PROPERTY.SEAS_ROUTE:
				self.setRoute(Route().parse(statement.getResource()))
				return
			
			# pass on to Object
			super(Waypoint, self).parse(statement)
		
