from SeasObjects.common.RESOURCE import RESOURCE

class ClassMapper(object):

	def __init__(self):
		
		from SeasObjects.model.Ability import Ability
		from SeasObjects.model.AbstractEntity import AbstractEntity
		from SeasObjects.model.Activity import Activity
		from SeasObjects.model.Address import Address
		from SeasObjects.model.AliveRequest import AliveRequest
		from SeasObjects.model.AliveResponse import AliveResponse
		from SeasObjects.model.Condition import Condition
		from SeasObjects.model.Controllability import Controllability
		from SeasObjects.model.Coordinates import Coordinates
		from SeasObjects.model.Device import Device
		from SeasObjects.model.Direction import Direction
		from SeasObjects.model.Entity import Entity
		from SeasObjects.model.Error import Error
		from SeasObjects.model.Evaluation import Evaluation
		from SeasObjects.model.Input import Input
		from SeasObjects.model.InterfaceAddress import InterfaceAddress
		from SeasObjects.model.Location import Location
		from SeasObjects.model.Map import Map
		from SeasObjects.model.Message import Message
		from SeasObjects.model.Notification import Notification
		from SeasObjects.model.Obj import Obj
		from SeasObjects.model.Organization import Organization
		from SeasObjects.model.Orientation import Orientation
		from SeasObjects.model.Output import Output
		from SeasObjects.model.Parameter import Parameter
		from SeasObjects.model.Person import Person
		from SeasObjects.model.PhysicalEntity import PhysicalEntity
		from SeasObjects.model.Provenance import Provenance
		from SeasObjects.model.Request import Request
		from SeasObjects.model.Response import Response
		from SeasObjects.model.Ring import Ring
		from SeasObjects.model.Route import Route
		from SeasObjects.model.Service import Service
		from SeasObjects.model.ServiceProvider import ServiceProvider
		from SeasObjects.model.Size import Size
		from SeasObjects.model.Velocity import Velocity
		from SeasObjects.model.Status import Status
		from SeasObjects.model.SystemOfInterest import SystemOfInterest
		from SeasObjects.model.TemporalContext import TemporalContext
		from SeasObjects.model.TimeSeries import TimeSeries
		from SeasObjects.model.ValueObject import ValueObject
		from SeasObjects.model.Variant import Variant
		from SeasObjects.model.Waypoint import Waypoint
		from SeasObjects.model.Waypoints import Waypoints
		from SeasObjects.model.Zone import Zone
		
		self.class_map = {
			RESOURCE.SEAS_ABILITY: Ability,
			RESOURCE.SEAS_ABSTRACTENTITY: AbstractEntity,
			RESOURCE.SEAS_ACTIVITY: Activity,
			RESOURCE.SEAS_ADDRESS: Address,
			RESOURCE.SEAS_ALIVEREQUEST: AliveRequest,
			RESOURCE.SEAS_ALIVERESPONSE: AliveResponse,
			RESOURCE.SEAS_CONDITION: Condition,
			RESOURCE.SEAS_CONTROLLABILITY: Controllability,
			RESOURCE.SEAS_COORDINATES: Coordinates,
			RESOURCE.SEAS_DEVICE: Device,
			RESOURCE.SEAS_DIRECTION: Direction,
			RESOURCE.SEAS_ENTITY: Entity,
			RESOURCE.SEAS_ERROR: Error,
			RESOURCE.SEAS_EVALUATION: Evaluation,
			RESOURCE.SEAS_INPUT: Input,
			RESOURCE.SEAS_INTERFACEADDRESS: InterfaceAddress,
			RESOURCE.SEAS_LOCATION: Location,
			RESOURCE.SEAS_MAP: Map,
			RESOURCE.SEAS_MESSAGE: Message,
			RESOURCE.SEAS_NOTIFICATION: Notification,
			RESOURCE.SEAS_OBJECT: Obj,
			RESOURCE.SEAS_ORGANIZATION: Organization,
			RESOURCE.SEAS_ORIENTATION: Orientation,
			RESOURCE.SEAS_OUTPUT: Output,
			RESOURCE.SEAS_PARAMETER: Parameter,
			RESOURCE.SEAS_PHYSICALENTITY: PhysicalEntity,
			RESOURCE.SEAS_PERSON: Person,
			RESOURCE.SEAS_PROVENANCE: Provenance,
			RESOURCE.SEAS_REQUEST: Request,
			RESOURCE.SEAS_RESPONSE: Response,
			RESOURCE.SEAS_RING: Ring,
			RESOURCE.SEAS_ROUTE: Route,
			RESOURCE.SEAS_SERVICE: Service,
			RESOURCE.SEAS_SERVICEPROVIDER: ServiceProvider,
			RESOURCE.SEAS_SIZE: Size,
			RESOURCE.SEAS_SPEED: Velocity,
			RESOURCE.SEAS_STATUS: Status,
			RESOURCE.SEAS_SYSTEM_OF_INTEREST: SystemOfInterest,
			RESOURCE.SEAS_TEMPORALCONTEXT: TemporalContext,
			RESOURCE.SEAS_TIMESERIES: TimeSeries,
			RESOURCE.SEAS_VALUEOBJECT: ValueObject,
			RESOURCE.SEAS_VARIANT: Variant,
			RESOURCE.SEAS_WAYPOINT: Waypoint,
			RESOURCE.SEAS_WAYPOINTS: Waypoints,
			RESOURCE.SEAS_ZONE: Zone
		}	
			
	def getClass(self, typelist, default = None):
		for t in typelist:
			if self.class_map.has_key(t):
				return self.class_map[t]
		
		# No match, return default
		return default
