import datetime

from model.connection import connection


# define the usertype id for differnet users
def user_type( user_id,description):
    a = connection()
    insert = a.initial()
    with insert.cursor() as cursor:
        now = datetime.datetime.now().date()
        sql = "INSERT INTO UserType (UserTypeID,Description) VALUES ( %s,%s)"
        cursor.execute(sql, (user_id,description,))
    insert.commit()
    insert.close()


# define qualifications for different users
def qualification(qual_id,description):
    a = connection()
    insert = a.initial()
    with insert.cursor() as cursor:
        now = datetime.datetime.now().date()
        sql = "INSERT INTO Qualification (QualificationID,Description) VALUES ( %s,%s)"
        cursor.execute(sql, (qual_id, description,))
    insert.commit()
    insert.close()


# define property values for different user
def property(property_id, name, description):
    connect = connection()
    insert = connect.initial()
    with insert.cursor() as cursor:
        sql = "INSERT INTO Property (PropertyID, Name, Description) VALUES ( %s,%s,%s)"
        cursor.execute(sql, (property_id, name, description,))
    insert.commit()
    insert.close()
user_type(1,'Admin')
user_type(2,'Moderator')
user_type(3,'Old User')
user_type(4, 'Middle User')
user_type(5,'New User')

qualification(1,'M.D')
qualification(2,'Ph.D')
qualification(3,'M.B.B.S')

property(1, "Distance_Run", "KM")
property(2, "Calories_Burnt", "Kcal")
property(3, 'Blood_Pressure', "mg")
property(4, 'Speed', "miles/hour")
