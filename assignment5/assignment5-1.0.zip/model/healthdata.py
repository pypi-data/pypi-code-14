import pymysql
import datetime

class healthdata_model:
    def healthdata_entry1(username,data):
        try:
            val1=0
            for i in range(0,len(data)):
                tmp=ord(data[i])
                val1=val1+tmp
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            now = str(datetime.datetime.now())
            # INSERT INTO COMMENT TABLE....................
            a = "insert into datum (DatumID,Username,PropertyID,Value,WhenSaved) VALUES(%s,%s,%s,%s,%s) "
            mycursor.execute(a, (val1,username,1,data,now))
            con.commit()
            mycursor.close()
            con.close()
        except:  # TO THROW AWAY ERRORS DUE TO WRONG INPUT....................
            raise RuntimeError
            #print("Input healthdata1 error")

    def healthdata_entry2(username,data):
        try:
            val2 = 0
            for i in range(0, len(data)):
                tmp = ord(data[i])
                val2 = val2 + tmp
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            now = str(datetime.datetime.now())
            # INSERT INTO COMMENT TABLE....................
            a = "insert into datum (DatumID,Username,PropertyID,Value,WhenSaved) VALUES(%s,%s,%s,%s,%s) "
            mycursor.execute(a, (val2,username,2,data,now))
            con.commit()
            mycursor.close()
            con.close()
        except:  # TO THROW AWAY ERRORS DUE TO WRONG INPUT....................
            #raise RuntimeError
            print("Input healthdata2 error")

class healthdata_view:
    def get_health(username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            now = str(datetime.datetime.now())
            # INSERT INTO COMMENT TABLE....................
            a = "Select Value from datum where Username=%s "
            mycursor.execute(a, (username))
            health=mycursor.fetchall()
            mycursor.close()
            con.close()
            return health
        except:  # TO THROW AWAY ERRORS DUE TO WRONG INPUT....................
            # raise RuntimeError
            print("healthdata error")

class health_friend:
    def get_friends1(username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            mycursor.execute("select Requested_Username from Friendship where Requester_Username=%s "
                             "and WhenUnfriended is null and WhenRejected is null and WhenConfirmed is not null", username)
            user_list = mycursor.fetchall()
            mycursor.close()
            con.close()
            return user_list
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("health fiend")

    def get_friends2(username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            mycursor.execute("select Requester_Username from Friendship where Requested_Username=%s "
                             "and WhenUnfriended is null and WhenRejected is null and WhenConfirmed is not null", username)
            user_list = mycursor.fetchall()
            mycursor.close()
            con.close()
            return user_list
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("health fiend")