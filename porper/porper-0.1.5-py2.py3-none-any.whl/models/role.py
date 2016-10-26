
import uuid

class Role:

    def __init__(self, connection):
        self.connection = connection

    def create(self, params):
        if not params.get('id'):
            params['id'] = str(uuid.uuid4())
        sql = "INSERT INTO roles (id, name) VALUES ('%s', '%s')" % (params['id'], params['name'])
        print sql
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        return params['id']

    def find(self, params):
        if params.get('id'):
            sql = "SELECT * FROM roles WHERE id = '%s'" % (params['id'])
        elif params.get('ids'):
            sql = "SELECT * FROM roles WHERE id IN ('%s')" % ("','".join(params['ids']))
        elif params.get('ids') == []:
            sql = "SELECT * FROM roles WHERE 1 = 0"
        else:
            sql = "SELECT * FROM roles"
        print sql
        rows = []
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            for row in cursor:
                rows.append({'id':row[0], 'name':row[1]})
        return rows
