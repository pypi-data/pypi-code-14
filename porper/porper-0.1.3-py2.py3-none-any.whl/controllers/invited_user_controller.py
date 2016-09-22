
from datetime import datetime

ADMIN_ROLE_ID = 'ffffffff-ffff-ffff-ffff-ffffffffffff'

class InvitedUserController:

    def __init__(self, connection):
        self.connection = connection
        from porper.models.invited_user import InvitedUser
        self.invited_user = InvitedUser(connection)
        from porper.models.user_role import UserRole
        self.user_role = UserRole(connection)
        from porper.controllers.token_controller import TokenController
        self.token_controller = TokenController(connection)

    def is_admin(self, user_id):
        row = self.user_role.find({'user_id': user_id, 'role_id': ADMIN_ROLE_ID})
        if len(row) > 0:  return True
        else: return False

    def is_role_admin(self, user_id, role_id):
        rows = self.user_role.find({'user_id': user_id, 'role_id': role_id})
        if len(rows) > 0 and rows[0]['is_admin']:  return True
        else: return False

    def create(self, access_token, params):

        rows = self.token_controller.find(access_token)
        user_id = rows[0]['user_id']

        # allowed if I'm an admin
        if self.is_admin(user_id):
            return self.save(user_id, params)

        # allowed if I'm the role admin of the given role
        role_id = params['role_id']
        if self.is_role_admin(user_id, role_id):
            return self.save(user_id, params)

        raise Exception("not permitted")

    def save(self, user_id, params):
        invited_users = self.invited_user.find(params)
        if len(invited_users) > 0:
            print 'already invited'
            return True
        if not params.get('invited_by'):
            params['invited_by'] = user_id
        if not params.get('invited_at'):
            params['invited_at'] = str(datetime.utcnow())
        if not params.get('state'):
            params['state'] = self.invited_user.INVITED
        if not params.get('is_admin'):
            params['is_admin'] = '0'
        return self.invited_user.create(params)

    def update(self, access_token, params):

        rows = self.token_controller.find(access_token)
        user_id = rows[0]['user_id']

        # allowed if I'm an admin
        if self.is_admin(user_id):
            return self.invited_user.update(params)

        # allowed if I'm the role admin of the given role
        role_id = params['role_id']
        if self.is_role_admin(user_id, role_id):
            return self.invited_user.update(params)

        raise Exception("not permitted")

    """
    1. return all invited users if I'm the admin
    2. return all invited users of a given role if I'm the role admin
    """
    def find_all(self, access_token, params):

        rows = self.token_controller.find(access_token)
        user_id = rows[0]['user_id']

        # return all invited users if I'm an admin
        if self.is_admin(user_id):  return self.invited_user.find({})

        if not params.get('role_id'):
            # return all invited users of roles where I'm the role admin
            user_roles = self.user_role.find({'user_id': user_id})
            role_ids = [ user_role['role_id'] for user_role in user_roles if user_role['is_admin'] ]
            if len(role_ids) > 0:   return self.invited_user.find({'role_ids': role_ids})
        else:
            # return all invited users of the given role if I'm the role admin
            role_id = params['role_id']
            if self.is_role_admin(user_id, role_id):    return self.invited_user.find(params)

        raise Exception("not permitted")
