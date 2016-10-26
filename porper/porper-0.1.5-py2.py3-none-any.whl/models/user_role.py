
class UserRole:

    def __init__(self, connection):
        self.connection = connection

    def create(self, params):
        if params.get('is_admin'):
            is_admin = 1
        else:
            is_admin = 0
        sql = "INSERT INTO users_roles (user_id, role_id, is_admin)"
        sql += " VALUES ('%s', '%s', %s)" % (params['user_id'], params['role_id'], is_admin)
        print sql
        with self.connection.cursor() as cursor:
            cursor.execute(sql)

    def find(self, params):
        sql = "SELECT * FROM users_roles"
        if params.get('user_id') and params.get('role_id'):
            sql += " WHERE user_id = '%s' AND role_id = '%s'" % (params.get('user_id'), params.get('role_id'))
        elif params.get('user_id'):
          sql += " WHERE user_id = '%s'" % (params.get('user_id'))
        elif params.get('role_id'):
          sql += " WHERE role_id = '%s'" % (params.get('role_id'))
        elif params.get('email'):
          sql = "SELECT ur.* FROM users_roles ur JOIN users u ON u.id = ur.user_id WHERE u.email = '%s'" % (params.get('email'))
        print sql
        rows = []
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            for row in cursor:
                rows.append({'id':row[0], 'user_id':row[1], 'role_id':row[2], 'is_admin':row[3]})
        return rows
