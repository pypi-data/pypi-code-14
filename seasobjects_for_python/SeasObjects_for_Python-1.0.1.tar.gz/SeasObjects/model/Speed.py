from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.CLASS import CLASS
from SeasObjects.rdf.Resource import Resource
from SeasObjects.model.Obj import Obj
from SeasObjects.model.ValueObject import ValueObject

from rdflib import XSD

import traceback

class Speed(Obj):
	
	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.linearSpeedX = None
		self.linearSpeedY = None
		self.linearSpeedZ = None
		self.angularSpeedX = None
		self.angularSpeedY = None
		self.angularSpeedZ = None
		self.groundSpeed = None
	
		self.setType(CLASS.SEAS_SPEED)
	
	def hasLinearSpeedX(self):
		return self.linearSpeedX is not None
	
	def setLinearSpeedX(self, l):
		self.linearSpeedX = l
	
	def getLinearSpeedX(self):
		return self.linearSpeedX
	
	def hasLinearSpeedY(self):
		return self.linearSpeedY is not None
	
	def setLinearSpeedY(self, l):
		self.linearSpeedY = l
	
	def getLinearSpeedY(self):
		return self.linearSpeedY
	
	def hasLinearSpeedZ(self):
		return self.linearSpeedZ is not None
	
	def setLinearSpeedZ(self, l):
		self.linearSpeedZ = l
	
	def getLinearSpeedZ(self):
		return self.linearSpeedZ
	
	def hasAngularSpeedX(self):
		return self.angularSpeedX is not None
	
	def setAngularSpeedX(self, l):
		self.angularSpeedX = l
	
	def getAngularSpeedX(self):
		return self.angularSpeedX

	def hasAngularSpeedY(self):
		return self.angularSpeedY is not None
	
	def setAngularSpeedY(self, l):
		self.angularSpeedY = l
	
	def getAngularSpeedY(self):
		return self.angularSpeedY
	
	def hasAngularSpeedZ(self):
		return self.angularSpeedZ is not None
	
	def setAngularSpeedZ(self, l):
		self.angularSpeedZ = l
	
	def getAngularSpeedZ(self):
		return self.angularSpeedZ
		
	def hasGroundSpeed(self):
		return self.groundSpeed is not None
	
	def setGroundSpeed(self, a):
		self.groundSpeed = a
	
	def getGroundSpeed(self):
		return self.groundSpeed
		
	def serialize(self, model):
		speed = super(Speed, self).serialize(model)
		
		if self.hasAngularSpeedX():
			speed.addProperty(model.createProperty( PROPERTY.SEAS_ANGULAR_SPEED_X ), self.getAngularSpeedX().serialize(model))
		if self.hasAngularSpeedY():
			speed.addProperty(model.createProperty( PROPERTY.SEAS_ANGULAR_SPEED_Y ), self.getAngularSpeedY().serialize(model))
		if self.hasAngularSpeedZ():
			speed.addProperty(model.createProperty( PROPERTY.SEAS_ANGULAR_SPEED_Z ), self.getAngularSpeedZ().serialize(model))

		if self.hasLinearSpeedX():
			speed.addProperty(model.createProperty( PROPERTY.SEAS_LINEAR_SPEED_X ), self.getLinearSpeedX().serialize(model))
		if self.hasLinearSpeedY():
			speed.addProperty(model.createProperty( PROPERTY.SEAS_LINEAR_SPEED_Y ), self.getLinearSpeedY().serialize(model))
		if self.hasLinearSpeedZ():
			speed.addProperty(model.createProperty( PROPERTY.SEAS_LINEAR_SPEED_Z ), self.getLinearSpeedZ().serialize(model))

		if self.hasGroundSpeed():
			speed.addProperty(model.createProperty( PROPERTY.SEAS_GROUND_SPEED ), self.getGroundSpeed().serialize(model))

		return speed
	
	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				speed = Speed(resource.toString())
			else:
				speed = Speed()
			speed.clearTypes()
			
			for statement in resource.findProperties():
				# parse statement
				speed.parse(statement);
			
			return speed
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
	
			# angularSpeedX
			if predicate == PROPERTY.SEAS_ANGULAR_SPEED_X:
				try:
					self.setAngularSpeedX(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:angularSpeedX value as literal double."
					traceback.print_exc()
				return
			
			# angularSpeedY
			if predicate == PROPERTY.SEAS_ANGULAR_SPEED_Y:
				try:
					self.setAngularSpeedY(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:angularSpeedY value as literal double."
					traceback.print_exc()
				return
			
			# angularSpeedZ
			if predicate == PROPERTY.SEAS_ANGULAR_SPEED_Z:
				try:
					self.setAngularSpeedZ(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:angularSpeedZ value as literal double."
					traceback.print_exc()
				return
				
			# linearSpeedX
			if predicate == PROPERTY.SEAS_LINEAR_SPEED_X:
				try:
					self.setLinearSpeedX(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:linearSpeedX value as literal double."
					traceback.print_exc()
				return
			
			# linearSpeedY
			if predicate == PROPERTY.SEAS_LINEAR_SPEED_Y:
				try:
					self.setLinearSpeedY(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:linearSpeedY value as literal double."
					traceback.print_exc()
				return
			
			# linearSpeedZ
			if predicate == PROPERTY.SEAS_LINEAR_SPEED_Z:
				try:
					self.setLinearSpeedZ(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:linearSpeedZ value as literal double."
					traceback.print_exc()
				return
			# groundSpeedX
			if predicate == PROPERTY.SEAS_GROUND_SPEED:
				try:
					self.setGroundSpeed(ValueObject().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:groundSpeed value as literal double."
					traceback.print_exc()
				return
				
			# pass on to Object
			super(Speed, self).parse(statement)
	