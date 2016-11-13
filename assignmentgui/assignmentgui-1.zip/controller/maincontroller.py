from model.friendship import Friendship
LARGE_FONT = ("Verdana", 12)
from model.admin import Admin
from model.enduser import User
from model.moderator import Moderator
from model.connection import connection


# login into the account
class login():
    def __init__(self):
        a = connection()
        self.insert = a.initial()

    def usertypeid(self,name):
        with self.insert.cursor() as cursor:
            sql = "SELECT UserTypeID FROM User WHERE Username=%s"
            cursor.execute(sql, (name))
            result = cursor.fetchone()
        user_id = (result['UserTypeID'])
        return user_id

    def logincheck(self,username,password):
        s = User()
        r=s.login(username,password)
        return r


# class that registers user
class UMRegister():
    def initial(self,username, primary_email, secondary_email, password, firstname, lastname, StreetNumber, StreetName,
                MajorMunicipality, GoverningDistrict, PostalArea, about_user, pic1, pic2, pic3):
        s=User()
        ms=s.initial(username, primary_email, secondary_email, password, firstname, lastname, StreetNumber, StreetName,
                MajorMunicipality, GoverningDistrict, PostalArea, about_user, pic1, pic2, pic3)
        return ms


# class that registers admin
class AMRegister():
    def initial(self,username, primary_email, secondary_email, password, firstname, lastname, StreetNumber, StreetName,
                MajorMunicipality, GoverningDistrict, PostalArea, about_user, pic1, pic2, pic3,phoneno):
        s=Admin()
        ms=s.initial(username, primary_email, secondary_email, password, firstname, lastname, StreetNumber, StreetName,
                MajorMunicipality, GoverningDistrict, PostalArea, about_user, pic1, pic2, pic3,phoneno)
        return ms


# class that registers moderator
class MMRegister():
    def initial(self,username, primary_email, secondary_email, password, firstname, lastname, StreetNumber, StreetName,
                MajorMunicipality, GoverningDistrict, PostalArea, about_user, pic1, pic2, pic3, phoneno,qualid):
        s = Moderator()
        ms=s.initial(username, primary_email, secondary_email, password, firstname, lastname, StreetNumber, StreetName,
                  MajorMunicipality, GoverningDistrict, PostalArea, about_user, pic1, pic2, pic3, phoneno,qualid)
        return ms




