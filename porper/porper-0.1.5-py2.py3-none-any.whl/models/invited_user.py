
class InvitedUser:

    def __init__(self, connection):
        self.connection = connection
        self.INVITED = 'invited'
        self.REGISTERED = 'registered'

    def create(self, params):
        sql = "INSERT INTO invited_users (email, role_id, invited_by, invited_at, state, is_admin)"
        sql += " VALUES ('%s', '%s', '%s', '%s', '%s', %s)" % (params['email'], params['role_id'], params['invited_by'], params['invited_at'], params['state'], params['is_admin'])
        print sql
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        return params['email']

    def update(self, params):
        sql = "UPDATE invited_users"
        sql += " SET state = '%s'" % (params['state'])
        sql += " WHERE email = '%s'" % (params['email'])
        print sql
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        return params['email']

    def find(self, params):
        sql = "SELECT iu.*, u.email invited_by_email, r.name role_name FROM invited_users iu"
        sql += " JOIN users u ON u.id = iu.invited_by"
        sql += " JOIN roles r ON r.id = iu.role_id"
        if params.get('email'):
            sql += " WHERE iu.email = '%s'" % (params['email'])
        elif params.get('role_id'):
            sql += " WHERE iu.role_id = '%s'" % (params['role_id'])
        elif params.get('role_ids'):
            sql += " WHERE iu.role_id IN ('%s')" % ("','".join(params['role_ids']))
        print sql
        rows = []
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            for row in cursor:
                rows.append({'id':row[0], 'email':row[1], 'role_id':row[2], 'invited_by':row[3], 'invited_at':str(row[4]), 'state':row[5], 'is_admin':row[6], 'invited_by_email':row[7], 'role_name':row[8]})
        return rows
