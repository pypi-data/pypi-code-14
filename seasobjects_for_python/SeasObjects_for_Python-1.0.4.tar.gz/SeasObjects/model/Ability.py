from SeasObjects.common.PROPERTY import PROPERTY
from Evaluation import Evaluation
from SeasObjects.rdf.Resource import Resource

class Ability(Evaluation):

	def __init__(self, uri = None):
		Evaluation.__init__(self, uri)
		self.isControlledBy = None
		self.condition = None
		self.setType(RESOURCE.SEAS_ABILITY)
	
	def serialize(self, model):
		resource = super(Ability, self).serialize(model)

		# isControlledBy
		if self.hasIsControlledBy():
			controlledBy = model.createResource(self.isControlledBy)
			resource.addProperty(model.createProperty( PROPERTY.SEAS_ISCONTROLLEDBY ), controlledBy)

		# condition
		if self.hasCondition():
			resource.addProperty(model.createProperty( PROPERTY.SEAS_HASCONDITION ), self.condition.serialize(model))

		return resource
	
	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				ability = Ability(resource.toString())
			else:
				ability = Ability()
			ability.clearTypes()
	
			for i in resource.findProperties():
				# parse statement
				ability.parse(i)
	
			return ability

		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
	
			# isControlledBy
			if predicate == PROPERTY.SEAS_ISCONTROLLEDBY:
				try:
					self.setIsControlledBy(statement.getResource().toString())
				except:
					print "Unable to interpret seas:isControlledBy value as resource."
					traceback.print_exc()
				return
	
			# condition
			if predicate == PROPERTY.SEAS_HASCONDITION:
				try:
					self.setCondition(Condition.parse(statement.getResource()))
				except:
					print "Unable to interpret seas:hasCondition value as resource."
					traceback.print_exc()
				return
	
			# pass on to Object
			super(Ability, self).parse(statement);

	def hasIsControlledBy(self):
		return self.isControlledBy is not None

	def getIsControlledBy(self):
		return self.isControlledBy;
	
	def setIsControlledBy(self, isControlledBy):
		self.isControlledBy = isControlledBy

	def hasCondition(self):
		return self.condition is not None
	
	def getCondition(self):
		return self.condition;

	def setCondition(self, condition):
		self.condition = condition
