import pymssql


class DBRead(object):
    # Database Read Class
    # __init__:     initializes connection to database using
    #               (host, user, password, database)
    # query:        queries statement and returns results
    # close:        closes MS SQL connection (IMPORTANT)

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = pymssql.connect(host, user, password, database)
        self.cursor = self.connection.cursor()

    def query(self, statement):
        self.cursor.execute(statement)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()


class DBWrite(DBRead):
    # Database Write Class - Inherits from DBRead
    # execute:      executes statement, commits changes,
    #               and returns results of statement

    def execute(self, statement):
        self.cursor.execute(statement)
        self.connection.commit()
