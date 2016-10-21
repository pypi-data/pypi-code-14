from arrowaimodel import ArrowAIModel
from arrowaiconnection import ArrowAIConnection
from model.tensorflow import TensorFlow
from data.data import Data

class ArrowAI(ArrowAIModel):
	def __init__(self, apiUser, apiKey):
		arrowAIConnection = ArrowAIConnection(apiKey, apiUser)
		self.tensorflow = TensorFlow(arrowAIConnection)
		self.data = Data(arrowAIConnection)