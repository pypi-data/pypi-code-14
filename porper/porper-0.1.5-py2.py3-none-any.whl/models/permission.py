
class Permission:

    def __init__(self, connection):
        self.connection = connection

    def create(self, params):
        user_id = params.get('user_id')
        role_id = params.get('role_id')
        if user_id:
            sql = "INSERT INTO permissions (user_id, action, resource, value, `condition`)"
            sql += " VALUES ('%s', '%s', '%s', '%s'" % (user_id, params.get('action'), params.get('resource'), params.get('value'))
        elif role_id:
            sql = "INSERT INTO permissions (role_id, action, resource, value, `condition`)"
            sql += " VALUES ('%s', '%s', '%s', '%s'" % (role_id, params.get('action'), params.get('resource'), params.get('value'))
        if params.get('condition'):
            sql += ", '%s')" % (params.get('condition'))
        else:
            sql += ", NULL)"
        print sql
        with self.connection.cursor() as cursor:
            cursor.execute(sql)

    def delete(self, params):
        if params.get('id'):
            sql = "DELETE FROM permissions WHERE id = %s" % (params.get('id'))
        else:
            sql = "DELETE FROM permissions "
            sql += " WHERE action = '%s' AND resource = '%s' AND value = '%s'" % (params.get('action'), params.get('resource'), params.get('value'))
            if params.get('user_id'):
                sql += " AND user_id = '%s'" % (params.get('user_id'))
            if params.get('role_id'):
                sql += " AND role_id = '%s'" % (params.get('role_id'))
        print sql
        with self.connection.cursor() as cursor:
            cursor.execute(sql)

    def find(self, params):
        sql = "SELECT * FROM permissions WHERE 1 = 1"
        if params.get('resource'):   sql += " AND resource = '%s'" % (params.get('resource'))
        if params.get('action'):   sql += " AND action = '%s'" % (params.get('action'))
        if params.get('value'):     sql += " AND (value = '%s' OR value = '*')" % (params.get('value'))
        if params.get('user_id'):
            if params.get('all'):
                sql += " AND (user_id = '%s' OR role_id IN (SELECT role_id FROM users_roles WHERE user_id = '%s'))" % (params.get('user_id'), params.get('user_id'))
            else:
                sql += " AND user_id = '%s'" % (params.get('user_id'))
        elif params.get('role_id'):
            sql += " AND role_id = '%s'" % (params.get('role_id'))
        print sql
        rows = []
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            for row in cursor:
                rows.append({'id':row[0], 'user_id':row[1], 'role_id':row[2], 'action':row[3], 'resource':row[4], 'value':row[5], 'condition':row[6]})
        return rows
