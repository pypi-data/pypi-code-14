from datastore_layer.models.property_types import PropertyTypes, create_property
from datastore_layer.models.dated_model_base import DatedModelBase


class Client(DatedModelBase):
    name = create_property(PropertyTypes.String, required=True)
    secret = create_property(PropertyTypes.String, default='', required=True)
    type = create_property(PropertyTypes.String, default='confidential', required=True)
    default_scope = create_property(PropertyTypes.String, default='', required=True)

    @property
    def default_scopes(self):
        if self.default_scope:
            return self.default_scope.split()
        return []

    @property
    def default_redirect_uri(self):
        return None

    @property
    def allowed_grant_types(self):
        return ['password', 'refresh_token', 'client_credentials']

    @property
    def client_id(self):
        return str(self.key.id())

    # json
    def json(self):
        return {'name': self.name,
                'client_id': str(self.key.id()),
                'client_secret': self.secret,
                'created': self.created.strftime("%Y-%m-%d %H:%M:%S"),
                'updated': self.updated.strftime("%Y-%m-%d %H:%M:%S")
                }
