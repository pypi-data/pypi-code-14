import datetime

import pymysql

from model.connection import connection
from model.friendship import Friendship
from model.people import People


# class to take entries of user
class User(People):

    def __init__(self):
        a = connection()
        self.insert = a.initial()
        super(User, self).__init__()

    def start(self, name):
        self.username = name

    def initial(self, username, primary_email, secondary_email, password, firstname, lastname, StreetNumber,StreetName,MajorMunicipality,GoverningDistrict,PostalArea, about_user, pic1, pic2, pic3):
        self.karma = 0
        self.user_typeid = 5
        self.long = 'new'
        self.type = 'user'
        self.username=username
        x=self.register(username,self.user_typeid, primary_email, secondary_email, password, firstname, lastname, StreetNumber,StreetName,MajorMunicipality,GoverningDistrict,PostalArea, about_user, pic1, pic2, pic3)
        #to find if duplicate data exists
        if x ==1:
            a = connection()
            self.insert = a.initial()
            try:
                with self.insert.cursor() as cursor:
                    now = datetime.datetime.now().date()
                    sql = "INSERT INTO EndUser (Username,Karma,DateCreated) VALUES ( %s,%s,%s)"
                    cursor.execute(sql, (self.username, self.karma, now,))
                    self.insert.commit()
                message=("Successfully registered!")

            except pymysql.err.IntegrityError:
                message=("this username already exist Duplicate problem")
            return message
        else:
            return "Usename already exist"

    # update the data about the user
    def update1(self):
            with self.insert.cursor() as cursor:
                sql = "SELECT DateCreated FROM EndUser,User WHERE EndUser.Username=%s and Status=%s "
                cursor.execute(sql, (self.username, 1,))
                dat = cursor.fetchone()
                datn=(dat['DateCreated'])
                if datn is not None:
                    today = datetime.datetime.now()
                    # Check if user is a month old
                    if datn.month - today.month == 1:
                        self.user_typeid = 4
                    # Check if user is an year old
                    elif datn.year - today.year >= 1:
                        self.user_typeid = 3
                    with self.insert.cursor() as cursor:
                        sql = "UPDATE User SET UserTypeID =%s WHERE Username=%s"
                        cursor.execute(sql, (self.user_typeid,self.username))
                        self.insert.commit()
                        return "your profile updated"
                else:
                    # display member as inactive
                    return "You are not an active member!"

    # function to store the score of the user
    def funkarma(self):
        response = input("What would you like to do?\n Post or Reply: ")
        # if a user is posting, increment karma by 2
        if response == "post" or response == "Post":
            self.karma += 2
            # else increment karma by 1
        elif response == "reply" or response == "Reply":
            self.karma += 1
        with self.insert.cursor() as cursor:
            sql = "UPDATE EndUser SET Karma=%s WHERE Username=%s "
            cursor.execute(sql, (self.karma , self.username))
            print("karma updated new karma is ",self.karma)
        self.insert.commit()

    # display the user data
    def display(self):
        # if user is active
        with self.insert.cursor() as cursor:
            sql = "SELECT EndUser.Username,Karma,UserTypeID,Email1,Email2,FirstName,LastName,AboutMe FROM EndUser,User" \
                  " WHERE EndUser.Username=User.Username and EndUser.Username=%s and Status=%s "
            cursor.execute(sql,( self.username, 1,))
            result = cursor.fetchone()
            if result is None:
                detail = "You are no longer an active member!"
            else:
                detail = result
        self.insert.commit()
        return detail

    def extract(self,):
        with self.insert.cursor() as cursor:
            sql = "SELECT Username,Karma,UserTypeID FROM EndUser,User" \
                  " WHERE EndUser.Username=User.Username and EndUser.Username=%s and Status=%s "
            cursor.execute(sql,( self.username, 1,))
            result = cursor.fetchone()

    def login_fun(self):
        print("enter login details of End User")
        email = input("enter email id")
        password = input("Enter password")
        self.login(email,password)

    # functions to send request , accept request ,withdraw the request , unfriend
    def sendrequest(self, name):
        f = Friendship(self.username)
        s=f.request(name)
        return s

    def acceptrequest(self):
        f = Friendship(self.username)
        str =f.accept()

    def withdrawnrequset(self,name):
        f=Friendship(self.username)
        str=f.withdrawn(name)
        return str

    def un_friend(self,name):
        f=Friendship(self.username)
        str=f.unfriend(name)
        return str

    def display_users(self,name):
        with self.insert.cursor() as cursor:
            sql = "SELECT Username FROM Enduser WHERE Username not in(%s) "
            cursor.execute(sql,name)
            result = cursor.fetchone()
        return result


    def end(self):
        self.insert.close()
