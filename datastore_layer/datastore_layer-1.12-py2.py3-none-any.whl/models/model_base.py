from google.appengine.ext import ndb
from property_types import PropertyTypes, create_property


# models should inherit from DatedModelBase instead of ModelBase
class ModelBase(ndb.Model):
    data_status = create_property(PropertyTypes.Boolean, required=True, default=True)

    # Query for active (not-deleted) models only
    @classmethod
    def query(cls, *args, **kwargs):
        status = kwargs.pop('status', True)
        return super(ModelBase, cls).query(cls.data_status == status, *args)

    # Query for active (not-deleted) models only
    @classmethod
    def get_by_id(cls, entity_id, status=True):
        entity = super(ModelBase, cls).get_by_id(entity_id)
        if entity and entity.data_status != status:
            return None
        return entity

    def put(self):
        return super(ModelBase, self).put()

    # DELETE
    def delete(self):
        self.data_status = False
        self.put()
        return self
