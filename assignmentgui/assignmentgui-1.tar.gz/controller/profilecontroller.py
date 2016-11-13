from model.admin import Admin
from model.connection import connection
from model.enduser import User
from model.moderator import Moderator
from model.people import People

# controller to display profile
class ProfileController:
    def __init__(self):
        a = connection()
        self.insert = a.initial()

    # display username
    def user_id(self,name):
        with self.insert.cursor() as cursor:
            sql = "SELECT UserTypeID FROM User WHERE Username=%s"
            cursor.execute(sql, (name))
            result = cursor.fetchone()
        user_id = (result['UserTypeID'])
        return user_id

    # display user_id
    def display(self,name,user_id):
        if user_id==1:
            s=Admin()
            s.start(name)
            detail=s.display()
        elif user_id==2:
            s=Moderator()
            s.start(name)
            detail = s.display()
        else:
            s=User()
            s.start(name)
            detail = s.display()
        return detail

    # update the profile of admin ,moderator ,user
    def update_profilea(self,name,phoneno):
        s=Admin()
        s.start(name)
        message=s.update_info(phoneno)
        return message

    def update_profilem(self,name,phoneno,qualification):
        s = Moderator()
        s.start(name)
        s.qualification_update(qualification)
        message = s.update_info(phoneno)
        return message

    def update_profileu(self,name):
        s = Moderator()
        s.start(name)
        message=s.update1()
        return message

    # deactivate the account
    def deactivate(self,name):
        s=People()
        s.startp(name)
        message=s.delete()
        return message


