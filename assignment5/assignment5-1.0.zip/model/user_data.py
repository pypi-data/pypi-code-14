import pymysql
import datetime

def get_user_data(username):
    try:
        con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
        mycursor = con.cursor()
        mycursor.execute("Select * from User WHERE Status=1 and Username=%s",username)
        names = mycursor.fetchall()
        mycursor.close()
        con.close()
        return names
    except:
        print("data error")

def del_userdetail(username):
    try:
        con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
        mycursor = con.cursor()
        mycursor.execute("update User SET Status=False WHERE Username=%s",username)
        con.commit()
        mycursor.close()
        con.close()
    except:
        print("delete error")