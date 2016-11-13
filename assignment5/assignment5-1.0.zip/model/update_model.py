import pymysql
import datetime

class update_model:
    def get_usertype(Username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            mycursor.execute("Select UserTypeID from User WHERE Username=%s and Status=1", Username)
            usertype = mycursor.fetchone()
            mycursor.close()
            con.close()
            return usertype
        except:
            print("error update")

    def update_Password(password,Username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            mycursor.execute("update User SET password=%s WHERE Username=%s", (password, Username))
            con.commit()
            mycursor.close()
            con.close()
        except:
            print("error update")

    def update_Email1(Email1,Username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            mycursor.execute("update User SET Email1=%s WHERE Username=%s", (Email1, Username))
            con.commit()
            mycursor.close()
            con.close()
        except:
            print("error update")

    def update_Email2(Email2,Username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            mycursor.execute("update User SET Email2=%s WHERE Username=%s", (Email2, Username))
            con.commit()
            mycursor.close()
            con.close()
        except:
            print("error update")

    def update_FirstName(FirstName,Username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            mycursor.execute("update User SET FirstName=%s WHERE Username=%s", (FirstName, Username))
            con.commit()
            mycursor.close()
            con.close()
        except:
            print("error update")

    def update_LastName(LastName,Username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            mycursor.execute("update User SET LastName=%s WHERE Username=%s", (LastName, Username))
            con.commit()
            mycursor.close()
            con.close()
        except:
            print("error update")