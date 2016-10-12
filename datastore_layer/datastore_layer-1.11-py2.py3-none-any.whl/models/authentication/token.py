from datetime import datetime, timedelta

from datastore_layer.models.authentication.client import Client
from datastore_layer.models.dated_model_base import DatedModelBase
from datastore_layer.models.property_types import PropertyTypes, create_property
from datastore_layer.models.user.user import User


class Token(DatedModelBase):
    access_token = create_property(PropertyTypes.String, required=True)
    refresh_token = create_property(PropertyTypes.String)
    client_key = create_property(PropertyTypes.Key, kind=Client, required=True)
    scope = create_property(PropertyTypes.String, required=True)
    expires = create_property(PropertyTypes.DateTime, required=True)
    user_key = create_property(PropertyTypes.Key, kind=User)
    token_type = create_property(PropertyTypes.String, required=True)

    # Init
    @classmethod
    def new(cls, **kwargs):
        token = cls()
        token.set_properties(**kwargs)
        return token

    def set_properties(self, **kwargs):
        expires_in = kwargs.pop('expires_in')
        if expires_in:
            self.set_expires(expires_in)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def set_expires(self, expires_in):
        self.expires = datetime.utcnow() + timedelta(seconds=expires_in)

    @property
    def user(self):
        if not self.user_key:
            return None
        return self.user_key.get()

    @property
    def user_id(self):
        if not self.user_key:
            return None
        return self.user_key.id()

    @property
    def client_id(self):
        return str(self.client_key.id())

    @property
    def scopes(self):
        if self.scope:
            return self.scope.split()
        return None
