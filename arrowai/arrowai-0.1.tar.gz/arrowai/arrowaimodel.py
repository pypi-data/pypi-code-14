from arrowaiconnection import ArrowAIConnection

class ArrowAIModel(ArrowAIConnection):
	def model_create(self, name):
		print ArrowAIConnection.getKey(self)

	def new_model(self):
		print ArrowAIConnection.getName(self)

