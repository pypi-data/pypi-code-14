import datetime
from abc import abstractmethod

import pymysql

from model.connection import connection


# the base class which holds the data of all kinds of user
class People(object):
    def __init__(self):
        a = connection()
        self.insert = a.initial()

    def startp(self, name):
        self.username = name

        # register the user
    def register(self, username, user_id, primary_email, secondary_email, password, firstname, lastname, StreetNumber, StreetName, MajorMunicipality, GoverningDistrict, PostalArea, about_user, pic1, pic2, pic3):
        self.active = 1
        self.username = username
        self.usertype_id = user_id
        self.primary_email = primary_email
        self.secondary_email = secondary_email
        self.password = password
        self.__firstname = firstname
        self.__lastname = lastname
        self.StreetNumber = StreetNumber
        self.StreetName = StreetName
        self.MajorMunicipality = MajorMunicipality
        self.GoverningDistrict = GoverningDistrict
        self.PostalArea = PostalArea
        self.about_user = about_user
        self.pic1 = pic1
        self.pic2 = pic2
        self.pic3 = pic3
        self.datn = datetime.datetime.now().date()
        a = connection()
        self.insert = a.initial()
        try:
            with self.insert.cursor() as cursor:
                sql = "INSERT INTO User ( Username,Password,Email1,Email2,FirstName,LastName,AboutMe,PhotoURL1,PhotoURL2,PhotoURL3,StreetNumber,StreetName,MajorMunicipality,GoverningDistrict,PostalArea,UserTypeID,Status)" \
                  " VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (self.username, self.password, self.primary_email,self.secondary_email,self.__firstname, self.__lastname, self.about_user, self.pic1, self.pic2, self.pic3, self.StreetName, self.StreetName,
                                 self.MajorMunicipality,
                                 self.GoverningDistrict,
                                 self.PostalArea,
                                 self.usertype_id,
                                 self.active,))
            self.insert.commit()
            return 1
        except pymysql.err.IntegrityError:
            message=("Username already existing")
            return message


    # for user login
    def login(self,email,password):
        with self.insert.cursor() as cursor:
            sql = "SELECT Username FROM User WHERE Username=%s and Password=%s and Status=%s"
            cursor.execute(sql, (email, password, 1,))
            result = cursor.fetchone()
            if result is None:
                self.session=0
            else:
                self.session=1
                return  result

        self.insert.commit()

# delete the user account
    def delete(self):
        with self.insert.cursor() as cursor:
            sql = "UPDATE User SET Status=%s WHERE Username=%s"
            cursor.execute(sql, (0,self.username,))
            message="Account Deactivated"
        self.insert.commit()
        return message

# update the user account
    def update(self,StreetNumber, StreetName, MajorMunicipality, GoverningDistrict, PostalArea):
        self.StreetNumber = StreetNumber
        self.StreetName = StreetName
        self.MajorMunicipality = MajorMunicipality
        self.GoverningDistrict = GoverningDistrict
        self.PostalArea = PostalArea
        with self.insert.cursor() as cursor:
            sql = "INSERT INTO User (StreetNumber,StreetName,MajorMunicipality,GoverningDistrict,PostalArea)" \
                  " VALUES ( %s,%s,%s,%s,%s)"
            cursor.execute(sql, (self.StreetName, self.StreetName,
                                 self.MajorMunicipality,
                                 self.GoverningDistrict,
                                 self.PostalArea,))
        self.insert.commit()
    @ abstractmethod
    def update1(self):
        pass

    def end(self):
        self.insert.close()

    def displayfunc(self):
        def display(self):
            # if user is active
            with self.insert.cursor() as cursor:
                sql = "SELECT Username,Email1,FirstName,LastName,AboutMe,UserTypeID FROM User"\
                      "WHERE Username=%s and Status=%s "
                cursor.execute(sql, (self.username, 1,))
                result = cursor.fetchone()
                if result is None:
                    return("You are no longer an active member!")
                else:
                    return(result)
            self.insert.commit()