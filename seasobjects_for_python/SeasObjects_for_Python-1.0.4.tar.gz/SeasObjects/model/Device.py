from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.model.PhysicalEntity import PhysicalEntity
from SeasObjects.rdf.Resource import Resource

import traceback

class Device(PhysicalEntity):

	def __init__(self, country_code, uri = None):
		PhysicalEntity.__init__(self, uri)
		self.country_code = country_code
		self.managingSystemUri = None
		self.setType(RESOURCE.SEAS_DEVICE);
	
	def hasManagingSystemUri(self):
		return self.managingSystemUri is not None

	def setManagingSystemUri(self, uri):
		self.managingSystemUri = uri
	
	def getManagingSystemUri(self):
		return self.managingSystemUri

	def serialize(self, model):
		device = super(Device, self).serialize(model)

		# set system uri
		if self.hasManagingSystemUri():
			system = model.createResource( self.managingSystemUri )
			device.addProperty(model.createProperty( PROPERTY.SEAS_ISMANAGEDBY ), system)

		return device

	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				device = Device(resource.toString())
			else:
				device = Device()
			device.clearTypes()
	
			for statement in resource.findProperties():
				device.parse(statement)
				
				return device
			
		else:
			# get predicate
			
			predicate = str(statement.getPredicate())

			# ismanagedby
			if predicate == PROPERTY.SEAS_ISMANAGEDBY:
				try:
					device.setManagingSystemUri(statement.getString())
				except:
					print "Unable to interpret seas:isManagedBy value as resource."
					traceback.print_exc()

			# pass on to Object
			super(Device, device).parse(statement)

