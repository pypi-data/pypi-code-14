import datetime

import pymysql

from model.connection import connection
# from model.people import People


# class for friendship
class Friendship:
    def __init__(self, name):
        self.name = name
        a = connection()
        self.insert = a.initial()

# send request
    def request(self, Requested_Username):
        a = connection()
        self.insert = a.initial()
        self.Requested_Username = Requested_Username
        with self.insert.cursor() as cursor:
            sql = "SELECT Email1 from User WHERE Username=%s and UserTypeID > 2 "
            cursor.execute(sql, (self.name,))
            result1 = cursor.fetchone()
            sql = "SELECT Username from User WHERE Username=%s and UserTypeID>2"
            cursor.execute(sql, self.Requested_Username)
            result2 = cursor.fetchone()
        # check if request is already sent
        if result1 is not None and result2 is not None:
            try:
                with self.insert.cursor() as cursor:
                    now = datetime.datetime.now().date()
                    sql = "INSERT INTO Friendship ( Requester_Username , Requested_Username" \
                          " ,WhenRequested) VALUES ( %s,%s,%s)"
                    cursor.execute(sql, (self.name, self.Requested_Username, now))
                self.insert.commit()
                s="Request Send"

            except pymysql.err.IntegrityError:
                s="You have already send a friend request to this user So cannot send it again"

        else:
            s="Both should be End User"
        return s

# accept to request
    def accept(self):
        with self.insert.cursor() as cursor:
            sql = "SELECT Requester_Username FROM Friendship WHERE Requested_Username=%s" \
                  " and WhenRejected IS NULL and WhenConfirmed IS NULL and WhenWithdrawn IS NULL"
            cursor.execute(sql, (self.name,))
            result = cursor.fetchall()
            self.insert.commit()
            return result

    def acceptupdate(self,p):
        with self.insert.cursor() as cursor:
            if p == 1:
                now = datetime.datetime.now().date()
                sql = "UPDATE Friendship SET WhenConfirmed =%s WHERE Requested_Username=%s " \
                  "and WhenRejected IS NULL and WhenConfirmed IS NULL and WhenWithdrawn IS NULL"
                cursor.execute(sql, (now, self.name,))
                str=" request confirmed"

            elif p == 2:
                now = datetime.datetime.now().date()
                sql = "UPDATE Friendship SET WhenRejected =%s WHERE Requested_Username=%s " \
                  "and WhenRejected IS NULL and WhenConfirmed IS NULL and WhenWithdrawn IS NULL"
                cursor.execute(sql, (now, self.name,))
                str="request rejected"
                # self.insert.commit()
            else:
                str = "no action taken"
            self.insert.commit()
            return str

# unfriend a friend in the friends' list


    def unfriend(self, name):
        with self.insert.cursor() as cursor:
            sql = "SELECT Requester_Username from Friendship WHERE Requested_Username in (%s,%s)" \
                  " and Requester_Username in (%s,%s) and WhenUnfriended IS NULL and WhenWithdrawn IS NULL and WhenConfirmed IS NOT NULL"
            cursor.execute(sql, (name, self.name,name,self.name))
            result = cursor.fetchone()
            if result is not None:
                with self.insert.cursor() as cursor:
                    now = datetime.datetime.now().date()
                    sql = "UPDATE Friendship SET WhenUnfriended =%s WHERE" \
                          " Requested_Username in (%s,%s) and Requester_Username in (%s,%s) and WhenConfirmed IS NOT NULL"
                    cursor.execute(sql, (now, self.name, name, self.name, name))
                str="you are no longer friend with "+name
                self.insert.commit()
            else:
                str="Cannot Unfriend again, you are already not friend"
            return str

# withdraw a friend request
    def withdrawn(self, name):
        with self.insert.cursor() as cursor:
            now = datetime.datetime.now().date()
            sql = "SELECT Requested_Username from Friendship WHERE Requested_Username =%s" \
                  " and Requester_Username=%s and WhenRejected IS NULL" \
                  " and WhenConfirmed IS NULL and WhenWithdrawn IS NULL"
            cursor.execute(sql, (name, self.name))
            result = cursor.fetchone()
            if result is not None:
                with self.insert.cursor() as cursor:
                    sql = "UPDATE Friendship SET WhenWithdrawn =%s" \
                          " WHERE Requested_Username=%s and Requester_Username=%s " \
                          "and WhenRejected IS NULL and WhenConfirmed IS NULL and WhenWithdrawn IS NULL"
                    cursor.execute(sql, (now, name, self.name))
                    str="you have withdraw your request from  "+name
                self.insert.commit()
            else:
                str="You cannot withdraw it now , Requested user has taken actions"
            return str

# to display the friends
    def display_friend(self):
        with self.insert.cursor() as cursor:
            now = datetime.datetime.now().date()
            sql = "SELECT Requester_Username from Friendship WHERE Requested_Username =%s" \
                  " and WhenRejected IS NULL" \
                  " and WhenConfirmed IS NOT NULL and WhenWithdrawn IS NULL and WhenUnfriended IS NULL"
            cursor.execute(sql, (self.name))
            result = cursor.fetchall()

            sql = "SELECT Requested_Username from Friendship WHERE Requester_Username =%s" \
                  " and WhenRejected IS NULL" \
                  " and WhenConfirmed IS NOT NULL and WhenWithdrawn IS NULL and WhenUnfriended IS NULL"
            cursor.execute(sql, (self.name))
            result1 = cursor.fetchall()

            p=[]
            for x in result:
                p.append(x["Requester_Username"])
            for x in result1:
                p.append(x["Requested_Username"])

        return p

# to display the list of people to whom we have sent a request
    def display_not_frnd_yet(self):
        with self.insert.cursor() as cursor:
            now = datetime.datetime.now().date()
            sql = "SELECT Requester_Username from Friendship WHERE Requested_Username =%s" \
                  " and WhenRequested IS NOT NULL and WhenRejected IS NULL" \
                  " and WhenConfirmed IS NULL and WhenWithdrawn IS NULL and WhenUnfriended IS NULL"
            cursor.execute(sql, (self.name))
            result = cursor.fetchall()

            sql = "SELECT Requested_Username from Friendship WHERE Requester_Username =%s" \
                  " and WhenRequested IS NOT NULL and WhenRejected IS NULL" \
                  " and WhenConfirmed IS NULL and WhenWithdrawn IS NULL and WhenUnfriended IS NULL"
            cursor.execute(sql, (self.name))
            result1 = cursor.fetchall()

            p = []
            for x in result:
                p.append(x["Requester_Username"])
            for x in result1:
                p.append(x["Requested_Username"])

        return p

    # end the connection
    def end(self):
        self.insert.close()

