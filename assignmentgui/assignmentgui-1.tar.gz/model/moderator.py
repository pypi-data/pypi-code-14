import datetime

import pymysql

from model.connection import connection
from model.people import People


# moderator class to receive entries of moderator
class Moderator(People):
    def __init__(self):
        a = connection()
        self.insert = a.initial()
        super(Moderator, self).__init__()

    def start(self, name):
        self.username = name

    def initial(self, username, primary_email, secondary_email, password, firstname, lastname,
                StreetNumber, StreetName, MajorMunicipality, GoverningDistrict, PostalArea, about_user, pic1, pic2,
                pic3, emegency_contact, i):
        self.type = 'mod'
        self.user_typeid = 2
        a = connection()
        self.insert = a.initial()
        x=self.register(username=username, user_id=self.user_typeid, primary_email=primary_email,
                      secondary_email=secondary_email, password=password, firstname=firstname, lastname=lastname,
                      StreetNumber=StreetNumber, StreetName=StreetName, MajorMunicipality=MajorMunicipality,
                      GoverningDistrict=GoverningDistrict, PostalArea=PostalArea, about_user=about_user, pic1=pic1,
                      pic2=pic2, pic3=pic3)
        self.emergency_contact = emegency_contact

        if x==1:
            try:
                with self.insert.cursor() as cursor:
                    sql = "INSERT INTO Moderator (Username,Phone) VALUES ( %s,%s)"
                    cursor.execute(sql, (self.username, self.emergency_contact,))
                self.insert.commit()
                self.qualification_update(i)
                return "Successfully registered!"
            except pymysql.err.IntegrityError:
                return "this username already in the Moderator"
        else:
            return "username already exist"

# method to update the qualification of a moderator
    def qualification_update(self, i):
        qual_id = None
        if i == 'M.B.B.S':
            qual_id = 3
        elif i == 'M.D':
            qual_id = 1
        elif i == 'Ph.D':
            qual_id = 2
        with self.insert.cursor() as cursor:
            now = datetime.datetime.now().date()
            sql = "INSERT INTO ModeratorQualification(QualificationID,Username,WhenAdded) VALUES ( %s,%s,%s)"
            cursor.execute(sql, (qual_id, self.username, now))
            self.insert.commit()

# update the emergency contact
    def update_info(self,emergency_contact):
        with self.insert.cursor() as cursor:
            sql = "UPDATE Administrator SET Phone=%s where Username=%s"
            cursor.execute(sql, (emergency_contact, self.username,))
        self.insert.commit()
        return (" info updated!!")

# display the details about the moderator
    def display(self):
        with self.insert.cursor() as cursor:
            sql = "SELECT Moderator.Username,UserTypeID ,Phone ,Email1,Email2,FirstName,LastName,AboutMe FROM Moderator,User " \
                  "WHERE Moderator.Username=User.Username and Moderator.Username=%s and Status=%s "
            cursor.execute(sql,( self.username, 1,))
            result = cursor.fetchone()
            if result is None:
                detail = "You are no longer an active member!"
            else:
                detail = result
        self.insert.commit()
        return detail


    def end(self):
        self.insert.close()
