from serverdensity.wrapper.crud import CRUD
from serverdensity.wrapper.jsonobject import JsonObject


class Dashboard(JsonObject, CRUD):

    _schemapath = '/schema/dashboards.json'

    PATHS = {
        'create': '/users/dashboards',
        'delete': '/users/dashboards/{}',
        'list': '/users/dashboards',
        'update': '/users/dashboards/{}',
        'view': '/users/dashboards/{}',
        'duplicate': '/users/dashboards/{}'
    }

    def duplicate(self, _id=None, **kwargs):
        if not _id:
            _id = self._id
        return self.__class__(self.api.post(url=self.PATHS['duplicate'].format(_id)))
