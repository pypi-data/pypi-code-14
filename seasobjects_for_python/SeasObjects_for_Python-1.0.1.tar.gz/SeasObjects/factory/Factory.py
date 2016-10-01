from SeasObjects.rdf.Model import Model


class Factory(object):

	def __init__(self):
		pass
	
	def createModel(self):
		return Model()

	"""
	 Set all namespaces declared in given class (e.g. NS) to the model.
	 @param model the model where namespaces are added
	 @param klazz class containing the namespaces as attributes
	"""
	def setNameSpaces(self, model, klazz):
		try:
			fields = klazz.getDeclaredFields();
			for field in fields:
				model.setNsPrefix(field.getName().toLowerCase(), field.get(klazz).toString())
		except:
			traceback.print_exc()
