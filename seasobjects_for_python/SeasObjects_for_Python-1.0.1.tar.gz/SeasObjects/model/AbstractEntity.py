from SeasObjects.model.Entity import Entity

class AbstractEntity(Entity):

	def __init__(self, uri = None):
		Entity.__init__(self, uri)
	
	def serialize(self, model):
		return super(AbstractEntity, self).serialize(model)
