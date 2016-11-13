import pymysql.cursors


# to establish connection to the database
class connection:
    def initial(self,):
        connection = pymysql.connect(host='localhost',
                             user='root',
                             password='ripul123',
                             db='smarthealthdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        return connection
