
import sys
sys.path.insert(0, r"..")

from porper.controllers.permission_controller import PermissionController
from porper.controllers.role_controller import RoleController
from porper.controllers.token_controller import TokenController
from porper.controllers.user_controller import UserController
from porper.controllers.user_role_controller import UserRoleController
from porper.controllers.invited_user_controller import InvitedUserController

ALLOWED_METHODS = [
    'create',
    'update',
    'delete',
    'find_all',
    'find_one'
]

ALLOWED_RESOURCES = [
    'permission',
    'role',
    'user',
    'user_role',
    'token',
    'invited_user'
]

def permission_handler(event, context):

    print event['oper']
    print event['params']

    oper = event.get('oper')
    if oper not in ALLOWED_METHODS: raise Exception("not supported method : %s" % oper)

    resource = event.get('resource')
    if resource not in ALLOWED_RESOURCES: raise Exception("not supported resource : %s" % resource)

    connection = None
    try:

        from porper.models.connection import mysql_connection
        connection = mysql_connection()
        print connection

        params = event.get('params')
        access_token = event.get('access_token').replace("Bearer ", "")
        controller = globals()['%sController' % resource.title().replace('_', '')](connection)
        ret = getattr(controller, oper)(access_token, params)
        connection.commit()
        print ret
        return ret
    except Exception, ex:
        print ex
        if connection:  connection.rollback()
        raise ex
