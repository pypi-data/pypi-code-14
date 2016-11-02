from SeasObjects.model.Evaluation import Evaluation
from SeasObjects.rdf.Resource import Resource
from SeasObjects.rdf.Statement import Statement
from SeasObjects.common.RESOURCE import RESOURCE

class Input(Evaluation):
	TYPE_DATA = 0
	TYPE_REFERENCE = 1
		
	def __init__(self, inputType = 0, uri = None):
		Evaluation.__init__(self, uri)
		self.inputType = inputType;
		self.setType(RESOURCE.SEAS_INPUT)
	
	def serialize(self, model):
		return super(Input, self).serialize(model)

	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				input = Input(resource.toString())
			else:
				input = Input()
			input.clearTypes()
			
			for i in resource.findProperties():
				# pass on to Evaluation
				input.parse(i)
			
			return input
		else:
			super(Input, self).parse(resource)

	def getInputType(self):
		return self.inputType
	
	def setInputType(self, inputType):
		self.inputType = inputType
