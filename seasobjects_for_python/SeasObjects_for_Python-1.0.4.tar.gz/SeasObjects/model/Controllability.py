from SeasObjects.model.Ability import Ability

class Controllability(Ability):

	def __init__(self, uri = None):
		Ability.__init__(self, uri)
		self.setType(RESOURCE.SEAS_CONTROLLABILITY)

	def parse(resource):
		if not resource.isAnon():
			controllability = Controllability(resource.toString())
		else:
			controllability = Controllability()
		controllability.clearTypes()

		for i in resource.findProperties():
			# parse statement
			controllability.parse(i)

		return controllability;

