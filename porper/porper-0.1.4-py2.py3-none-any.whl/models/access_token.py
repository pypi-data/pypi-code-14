
class AccessToken:

    def __init__(self, connection):
        self.connection = connection

    def create(self, params):
        sql = "INSERT INTO tokens (access_token, refresh_token, refreshed_time, user_id) VALUES ('" + params['access_token'] + "', '" + params['refresh_token'] + "', '" + params['refreshed_time'] + "', '" + params['user_id'] + "')"
        print sql
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        return params['access_token']

    def update(self, params):
        sql = "UPDATE tokens SET refresh_token = '" + params['refresh_token'] + "', refreshed_time = '" + params['refreshed_time'] + "' WHERE access_token = '" + params['access_token'] + "'"
        print sql
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        return params['access_token']

    def find(self, params):
        sql = "SELECT * FROM tokens WHERE access_token = '" + params['access_token'] + "'"
        print sql
        rows = []
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            for row in cursor:
                rows.append({'access_token':row[0], 'refresh_token':row[1], 'refreshed_time':str(row[2]), 'user_id':row[3]})
        return rows
