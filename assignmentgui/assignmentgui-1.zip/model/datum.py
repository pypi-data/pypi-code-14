from model.connection import connection
import datetime
from abc import abstractmethod
import pymysql
import uuid


class Datum(object):

    def __init__(self):
        connect = connection()
        self.insert = connect.initial()

    def datum(self, name, property_id, value,datum_id=None):
        connect = connection()
        self.insert = connect.initial()
        self.datum_id = uuid.uuid4().hex if datum_id is None else datum_id
        try:
            with self.insert.cursor() as cursor:
                when_created = datetime.datetime.utcnow()
                sql = "INSERT INTO Datum ( DatumID, Username, PropertyID, Value, WhenSaved)" \
                      " VALUES ( %s, %s, %s, %s, %s)"
                cursor.execute(sql, (datum_id, name, property_id, value, when_created))
                sql = "Select * from Datum where DatumID = %s "
                cursor.execute(sql , datum_id)
                ret = cursor.fetchall()
                self.insert.commit()
                print("success")
        except pymysql.err.IntegrityError:
            #  username already existing error
             print("DatumID exist")
# display the health data of user
    def display(self,username):
        # if user is active
        with self.insert.cursor() as cursor:
            sql = "SELECT Username , PropertyID , Value  FROM Datum Where Username = %s"
            cursor.execute(sql,username)
            result = cursor.fetchall()
            return result
# display the health data of friend

    def display_friend_info(self,username,friendname):

        with self.insert.cursor() as cursor:
            sql1 = "SELECT * FROM Friendship" \
                   " Where (Requester_Username =%s AND Requested_Username = %s and WhenUnfriended IS NULL and WhenConfirmed is NOT NULL )  "
            cursor.execute(sql1, (username, friendname))
            result1 = cursor.fetchone()
            #  return ["Name :" + result["Username"]+ "\n" +  result["PropertyID"],result["Value"],]
            sql2 = "SELECT WhenConfirmed , WhenUnfriended , WhenRejected , WhenWithdrawn FROM Friendship" \
                   " Where (Requester_Username =%s AND Requested_Username = %s and WhenUnfriended IS NULL and WhenConfirmed is NOT NULL)  "
            cursor.execute(sql2, (friendname, username))
            result2 = cursor.fetchone()

            if (result1 is not None) or (result2 is not None):
                with self.insert.cursor() as cursor:
                    sql = "SELECT Username , PropertyID , Value  FROM Datum Where Username = %s"
                    cursor.execute(sql, friendname)
                    result = cursor.fetchall()
            else:
                result="You are not a friend"
            return result

