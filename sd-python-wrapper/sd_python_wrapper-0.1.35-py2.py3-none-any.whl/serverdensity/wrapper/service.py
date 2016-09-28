from serverdensity.wrapper.jsonobject import JsonObject
from serverdensity.wrapper.crud import CRUD


class Service(JsonObject, CRUD):

    _schemapath = '/schema/services.json'

    PATHS = {
        'create': '/inventory/services',
        'delete': '/inventory/services/{}',
        'list': '/inventory/services',
        'search': '/inventory/resources',
        'update': '/inventory/services/{}',
        'view': '/inventory/services/{}',
        'groups': '/inventory/services/groups'
    }

    def search(self, filtering, **kwargs):
        kwargs.setdefault('params', {})['filter'] = filtering
        result = self.api.get(url=self.PATHS['search'], **kwargs)
        return [self.__class__(item) for item in result]

    def groups(self, **kwargs):
        return self.api.get(url=self.PATHS['groups'])
