
ALL = "*"

class ResourceController():

    def __init__(self, account_id, region, permission_connection):
        self.account_id = account_id
        self.region = region
        self.connection = permission_connection
        self.resource = None
        self.model = None
        from porper.controllers.permission_controller import PermissionController
        self.permission_controller = PermissionController(self.connection)

    @property
    def model_name(self):
        return self.model.__class__.__name__

    def _find_permitted(self, access_token, action, id=None):
        params = {
            'action': action,
            'resource': self.resource,
            'all': True
        }
        if id: params['value'] = id
        permissions = self.permission_controller.find_all(access_token, params)
        print 'permissions : %s' % permissions
        return permissions

    def is_permitted(self, access_token, action, id):
        #permissions = self._find_permitted(access_token, action, id)
        #return len(permissions) > 0
        params = {
            'action': action,
            'resource': self.resource,
            'all': True,
            'value': id
        }
        return self.permission_controller.is_permitted(access_token, params)

    def create(self, access_token, params):
        if not self.is_permitted(access_token, 'create', params['id']):    raise Exception("not permitted")
        ret = self.model.create(params)
        print "%s is successfully created : %s" % (self.model_name, ret)
        return ret

    def update(self, access_token, params):
        if not self.is_permitted(access_token, 'update', params['id']):    raise Exception("not permitted")
        ret = self.model.update(params)
        print "%s [%s] is successfully updated : %s" % (self.model_name, params['id'], ret)
        return ret

    def delete(self, access_token, params):
        if not self.is_permitted(access_token, 'delete', params['id']):    raise Exception("not permitted")
        ret = self.model.delete(params)
        print "%s [%s] is successfully deleted : %s" % (self.model_name, params['id'], ret)
        return ret

    # find all read-permitted instances of the current resource, so 'id' is NOT given
    def find_all(self, access_token, params=None):
        permissions = self._find_permitted(access_token, 'read')
        if len(permissions) == 0:   raise Exception("not permitted")
        ids = [ permission['value'] for permission in permissions ]
        if not params:  params = {}
        if ALL not in ids:  params['ids'] = ids
        return self.model.find(params)

    # find one read-permitted instance of the current resource whose id is the given
    def find_one(self, access_token, params):
        permissions = self._find_permitted(access_token, 'read', params['id'])
        if len(permissions) == 0:   raise Exception("not permitted")
        for permission in permissions:
            if permission['value'] == params['id'] or permission['value'] == ALL:
                return self.model.find({'id': params['id']})
        raise Exception("not permitted")
