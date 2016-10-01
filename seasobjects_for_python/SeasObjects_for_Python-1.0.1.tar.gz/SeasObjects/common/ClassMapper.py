from SeasObjects.common.CLASS import CLASS

class ClassMapper(object):

	def __init__(self):
		
		from SeasObjects.model.Ability import Ability
		from SeasObjects.model.AbstractEntity import AbstractEntity
		from SeasObjects.model.Activity import Activity
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
		from SeasObjects.model.Orientation import Orientation
		from SeasObjects.model.Output import Output
		from SeasObjects.model.Parameter import Parameter
		from SeasObjects.model.PhysicalEntity import PhysicalEntity
		from SeasObjects.model.Provenance import Provenance
		from SeasObjects.model.Request import Request
		from SeasObjects.model.Response import Response
		from SeasObjects.model.Ring import Ring
		from SeasObjects.model.Route import Route
		from SeasObjects.model.Service import Service
		from SeasObjects.model.ServiceProvider import ServiceProvider
		from SeasObjects.model.Size import Size
		from SeasObjects.model.Speed import Speed
		from SeasObjects.model.Status import Status
		from SeasObjects.model.SystemOfInterest import SystemOfInterest
		from SeasObjects.model.TemporalContext import TemporalContext
		from SeasObjects.model.TimeSeries import TimeSeries
		from SeasObjects.model.ValueObject import ValueObject
		from SeasObjects.model.Variant import Variant
		from SeasObjects.model.Waypoint import Waypoint
		from SeasObjects.model.Waypoints import Waypoints
			
		self.class_map = {
			CLASS.SEAS_ABILITY: Ability,
			CLASS.SEAS_ABSTRACTENTITY: AbstractEntity,
			CLASS.SEAS_ACTIVITY: Activity,
			CLASS.SEAS_ALIVEREQUEST: AliveRequest,
			CLASS.SEAS_ALIVERESPONSE: AliveResponse,
			CLASS.SEAS_CONDITION: Condition,
			CLASS.SEAS_CONTROLLABILITY: Controllability,
			CLASS.SEAS_COORDINATES: Coordinates,
			CLASS.SEAS_DEVICE: Device,
			CLASS.SEAS_DIRECTION: Direction,
			CLASS.SEAS_ENTITY: Entity,
			CLASS.SEAS_ERROR: Error,
			CLASS.SEAS_EVALUATION: Evaluation,
			CLASS.SEAS_INPUT: Input,
			CLASS.SEAS_INTERFACEADDRESS: InterfaceAddress,
			CLASS.SEAS_LOCATION: Location,
			CLASS.SEAS_MAP: Map,
			CLASS.SEAS_MESSAGE: Message,
			CLASS.SEAS_NOTIFICATION: Notification,
			CLASS.SEAS_OBJECT: Obj,
			CLASS.SEAS_ORIENTATION: Orientation,
			CLASS.SEAS_OUTPUT: Output,
			CLASS.SEAS_PARAMETER: Parameter,
			CLASS.SEAS_PHYSICALENTITY: PhysicalEntity,
			CLASS.SEAS_PROVENANCE: Provenance,
			CLASS.SEAS_REQUEST: Request,
			CLASS.SEAS_RESPONSE: Response,
			CLASS.SEAS_RING: Ring,
			CLASS.SEAS_ROUTE: Route,
			CLASS.SEAS_SERVICE: Service,
			CLASS.SEAS_SERVICEPROVIDER: ServiceProvider,
			CLASS.SEAS_SIZE: Size,
			CLASS.SEAS_SPEED: Speed,
			CLASS.SEAS_STATUS: Status,
			CLASS.SEAS_SYSTEM_OF_INTEREST: SystemOfInterest,
			CLASS.SEAS_TEMPORALCONTEXT: TemporalContext,
			CLASS.SEAS_TIMESERIES: TimeSeries,
			CLASS.SEAS_VALUEOBJECT: ValueObject,
			CLASS.SEAS_VARIANT: Variant,
			CLASS.SEAS_WAYPOINT: Waypoint,
			CLASS.SEAS_WAYPOINTS: Waypoints
		}	
			
	def getClass(self, typelist, default = None):
		for t in typelist:
			if self.class_map.has_key(t):
				return self.class_map[t]
		
		# No match, return default
		return default
	
		