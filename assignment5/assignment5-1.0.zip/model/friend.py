import pymysql
import datetime

class friend_send:
    def send_get_username(temp):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            mycursor.execute("Select Username from User WHERE UserTypeID=1 and Status=1")
            names = mycursor.fetchall()
            mycursor.close()
            con.close()
            return names
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("hh")
            raise RuntimeError

    def send_req(reqr_username,reqd_username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            now =str(datetime.datetime.now())
            a = "insert into friendship(Requester_Username, Requested_Username, WhenRequested) VALUES(%s,%s,%s)"
            mycursor.execute(a, (reqr_username, reqd_username, now))
            con.commit()
            mycursor.close()
            con.close()
            return True
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            return False
            #raise RuntimeError

    def can_send(reqr_username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            user_list_check=mycursor.execute("select Requested_Username from Friendship where Requester_Username=%s "
                             "and WhenConfirmed is NULL and WhenRejected is NULL and WhenRequested is NULL ", reqr_username)
            #user_list_check = mycursor.fetchall()
            con.commit()
            mycursor.close()
            con.close()
            return user_list_check
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("hha")
            #raise RuntimeError

    def send_check_user(username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            name1=mycursor.execute("Select Username from User WHERE Username=%s and Status=1 and UserTypeID=1", username)
            mycursor.close()
            con.close()
            return name1
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("hh")
            #raise RuntimeError


class accept_friend:
    def accept_pending(reqd_username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            mycursor.execute("Select Requester_Username from Friendship where Requested_Username=%s "
                             "and WhenRejected is null and WhenConfirmed is null and WhenWithdrawn is null", reqd_username)
            user_pending=mycursor.fetchall()
            mycursor.close()
            con.close()
            return user_pending
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("NO requests to approve")

    def accept_req(reqr_username,reqd_username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            now = str(datetime.datetime.now())
            mycursor.execute("update Friendship SET WhenConfirmed=%s WHERE Requested_Username=%s and Requester_Username=%s",
                             (now, reqd_username, reqr_username))
            con.commit()
            mycursor.close()
            con.close()
        except:
            print("bggg")


class rejetc_friend:
    def reject_pending(reqd_username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            mycursor.execute("Select Requester_Username from Friendship where Requested_Username=%s "
                             "and WhenRejected is null and WhenConfirmed is null and WhenWithdrawn is null", reqd_username)
            user_pending=mycursor.fetchall()
            mycursor.close()
            con.close()
            return user_pending
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("NO requests to disapprove")

    def reject_req(reqr_username,reqd_username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            now = str(datetime.datetime.now())
            mycursor.execute("update Friendship SET WhenRejected=%s WHERE Requested_Username=%s and Requester_Username=%s",
                             (now, reqd_username, reqr_username))
            con.commit()
            mycursor.close()
            con.close()
        except:
            print("bggwdeg")


class withdraw_friend:
    def withdraw_sent(username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            now = str(datetime.datetime.now())
            mycursor.execute("select Requested_Username from Friendship where Requester_Username=%s "
                             "and WhenConfirmed is null and WhenRejected is null and WhenWithdrawn is null "
                             "and WhenRequested is not null",username)
            user_list=mycursor.fetchall()
            mycursor.close()
            con.close()
            return user_list
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            raise RuntimeError
            print("NO requests with")

    def withdraw_req(reqr_username,reqd_username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            now = str(datetime.datetime.now())
            mycursor.execute("update Friendship SET WhenWithdrawn=%s WHERE Requested_Username=%s and Requester_Username=%s",
                             (now, reqr_username, reqd_username))
            con.commit()
            mycursor.close()
            con.close()
        except:
            print("no withdraw")


class unfriend_friend:
    def unfriend_it(username):
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
            print("NO unfiend")

    def unfriend_it2(username):
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
            print("NO unfiend")

    def unfriend_req(reqr_username,reqd_username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            now = str(datetime.datetime.now())
            mycursor.execute("update Friendship SET WhenUnfriended=%s WHERE Requested_Username=%s and Requester_Username=%s",
                (now, reqd_username, reqr_username))
            con.commit()
            mycursor.close()
            con.close()
        except:
            print("bgbffgbgg")