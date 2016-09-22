
ADMIN_ROLE_ID = 'ffffffff-ffff-ffff-ffff-ffffffffffff'

class UserController:

    def __init__(self, connection):
        self.connection = connection
        from porper.models.user import User
        from porper.models.user_role import UserRole
        from porper.models.invited_user import InvitedUser
        self.user = User(connection)
        self.user_role = UserRole(connection)
        self.invited_user = InvitedUser(connection)
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

    def is_member(self, user_id, role_id):
        rows = self.user_role.find({'user_id': user_id, 'role_id': role_id})
        if len(rows) > 0:  return True
        else: return False

    def create(self, access_token, params):

        # if this is the first user, save it as an admin
        users = self.user.find({})
        if len(users) == 0:
            # set this user to the admin
            self.user.create(params)
            self.user_role.create({'user_id': params['id'], 'role_id': ADMIN_ROLE_ID})
            return params['id']

        # add a user to a role if I'm an admin or the role admin of the given role
        if params.get('role_id'):
            rows = self.token_controller.find(access_token)
            user_id = rows[0]['user_id']
            if self.is_admin(user_id) or self.is_role_admin(user_id, role_id):
                self.user_role.create(params)
                return user_id
            else:
                raise Exception("not permitted")

        rows = self.user.find(params)
        if len(rows) > 0:
            print 'already exists'
            return rows[0]['id']

        # add the user if this user was invited before
        invited_users = self.invited_user.find(params)
        if len(invited_users) == 1:
            invited_user = invited_users[0]
            self.user.create(params)
            self.user_role.create({'user_id': params['id'], 'role_id': invited_user['role_id'], 'is_admin': invited_user['is_admin']})
            self.invited_user.update({'email':params['email'], 'state':self.invited_user.REGISTERED})
            return params['id']
        else:
            raise Exception("not permitted")

    """
    1. return requested users if I'm the admin
    2. return all users of roles where I'm the role admin
    3. return myself if I'm not the role admin of any role
    4. return all members of the given role if I'm a member of the given role
    """
    def find_all(self, access_token, params):

        rows = self.token_controller.find(access_token)
        user_id = rows[0]['user_id']

        # return all users if I'm an admin
        if self.is_admin(user_id):  return self.user.find(params)

        if not params.get('role_id'):
            # return all users of roles where I'm the role admin
            user_roles = self.user_role.find({'user_id': user_id})
            role_ids = [ user_role['role_id'] for user_role in user_roles if user_role['is_admin'] ]
            if len(role_ids) > 0:   return self.user.find({'role_ids': role_ids})

            # if role is not given, return only itself
            return self.user.find({'id': user_id})

        # return all members of the given role if I'm a member of the given role
        if self.is_member(user_id, params['role_id']):  return self.user.find(params)

        raise Exception("not permitted")
