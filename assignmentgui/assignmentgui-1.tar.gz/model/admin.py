import pymysql

from model.connection import connection
from model.people import People


# admin class
class Admin(People):
    def __init__(self):
        a = connection()
        self.insert = a.initial()
        super(Admin, self).__init__()

    def start(self, name):
        self.username = name

# receive the entries of the admin
    def initial(self, username, primary_email, secondary_email, password, firstname, lastname, StreetNumber, StreetName,
                MajorMunicipality, GoverningDistrict, PostalArea, about_user, pic1, pic2, pic3, emegency_contact):
        self.type = 'admin'
        self.user_typeid = 1
        a = connection()
        self.insert = a.initial()
        x=self.register(username, self.user_typeid, primary_email, secondary_email, password, firstname, lastname,
                      StreetNumber, StreetName, MajorMunicipality, GoverningDistrict, PostalArea, about_user, pic1,
                      pic2, pic3)
        self.emergency_contact = emegency_contact

        # check if there similar data exists else store the newly entered data
        if x==1:
            try:
                with self.insert.cursor() as cursor:
                    sql = "INSERT INTO Administrator (Username,Phone) VALUES ( %s,%s)"
                    cursor.execute(sql, (self.username, self.emergency_contact,))
                    self.insert.commit()
                return "Successfully registered!"
            except pymysql.err.IntegrityError:
                return "this username already Exist Duplicate Problem"
        else:
            return "username already exist"

    # update phone number in profile
    def update_info(self,phoneno):
        with self.insert.cursor() as cursor:
            sql = "UPDATE Administrator SET Phone=%s where Username=%s"
            cursor.execute(sql, (phoneno, self.username,))
        self.insert.commit()
        return "info updated!!"

    # display the details of the profile
    def display(self):
        with self.insert.cursor() as cursor:
            sql = "SELECT Administrator.Username,UserTypeID FROM Administrator,User " \
                  "WHERE Administrator.Username=User.Username and Administrator.Username=%s and Status=%s "
            cursor.execute(sql, (self.username, 1,))
            result = cursor.fetchone()
            if result is None:
                detail = "You are no longer an active member!"
            else:
                detail = result
        self.insert.commit()
        return detail

    def end(self):
        self.insert.close()
