import pymysql

class signin_model:
    def query_signin(username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            a = "select Password from user where Username=%s and Status=1"
            mycursor.execute(a, username)
            check = mycursor.fetchone()
            mycursor.close()
            con.close()
            return check

        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("signin model error")

    def ForeignKey(temp):  # temporary making foreign key constraint as zero
        con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
        mycursor = con.cursor()
        sql = "set global foreign_key_checks=0"  # temporary making foreign key constraints as zero
        mycursor.execute(sql)
        con.commit()
        mycursor.close()
        con.close()
