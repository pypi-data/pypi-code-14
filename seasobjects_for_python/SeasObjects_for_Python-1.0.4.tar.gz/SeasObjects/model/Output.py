from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.model.Evaluation import Evaluation

class Output(Evaluation):

	def __init__(self, uri = None):
		Evaluation.__init__(self, uri)
		self.availabilities = []
		self.dataAvailabilities = []
		self.setType(RESOURCE.SEAS_OUTPUT)
	
	def serialize(self, model):
		output = super(Output, self).serialize(model)
		
		# availability
		availabilityProp = model.createProperty( PROPERTY.SEAS_HASAVAILABILITY )
		for availability in self.availabilities:
			output.addProperty( availabilityProp, availability.serialize(model) )

		# data availability
		dataAvailabilityProp = model.createProperty( PROPERTY.SEAS_HASDATAAVAILABILITY )
		for availability in self.dataAvailabilities:
			output.addProperty( dataAvailabilityProp, availability.serialize(model) )

		return output


	def parse(self, resource):
		from SeasObjects.model.Availability import Availability
		
		if not resource.isAnon():
			output = Output(resource.toString())
		else:
			output = Output()
		output.clearTypes()
		
		for statement in resource.findProperties():
			# get predicate
			predicate = str(statement.getPredicate())

			# availability
			if predicate == PROPERTY.SEAS_HASAVAILABILITY:
				try:
					output.addAvailability(Availability().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:hasAvailability value as resource."
					traceback.print_exc()
				continue

			# data availability
			if predicate == PROPERTY.SEAS_HASDATAAVAILABILITY:
				try:
					output.addDataAvailability(Availability().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:hasDataAvailability value as resource."
					traceback.print_exc()
				continue

			# pass on to Evaluation
			super(Output, output).parse(statement)
		
		return output


	def hasAvailability(self):
		return len(self.availabilities) > 0
	
	def getAvailabilities(self):
		return self.availabilities
	
	def addAvailability(self, availability):
		self.availabilities.add(availability)

	def hasDataAvailability(self):
		return len(self.dataAvailabilities) > 0
	
	def getDataAvailabilities(self):
		return self.dataAvailabilities
	
	def addDataAvailability(self, availability):
		self.dataAvailabilities.add(availability)

