import pymysql
import datetime

class register_model:
    def check_name(username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            # FUNCTION TO CHECK FOR UNIQUE USERNAME........
            a = "select Username from user where Username=%s"
            mycursor.execute(a, username)
            check = mycursor.fetchone()
            if check!=None:
                if(check[0]==username):
                    return False
                else:
                    return True
            else:
                return True
        except:
            raise RuntimeError
            print("username error")

    def reg_enduser(data):
        try:
            now = str(datetime.datetime.now().date())
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            # INSERTION INTO USER TABLE............
            b = "insert into user(Username, Password, Email1, Email2, FirstName, LastName," \
                " AboutMe, PhotoURL1, PhotoURL2, PhotoURL3, StreetNumber, StreetName, MajorMunicipality," \
                " GoverningDistrict, PostalArea, UserTypeID, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(b, (
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
                data[11],data[12], data[13], data[14], 1, data[15]))
            # INSERTION INTO ENDUSER TABLE
            c = "insert into enduser (Username,Karma,DateCreated) VALUES(%s,%s,%s) "
            mycursor.execute(c, (data[0], 1, now))
            con.commit()
            mycursor.close()
            con.close()
        except:  # TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("INPUT error")
            #raise RuntimeError

    def reg_mod(data):
        try:
            now = str(datetime.datetime.now().date())
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            b = "insert into user(Username, Password, Email1, Email2, FirstName, LastName, AboutMe, PhotoURL1," \
                " PhotoURL2, PhotoURL3, StreetNumber, StreetName, MajorMunicipality, GoverningDistrict, PostalArea," \
                " UserTypeID, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(b, (
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
                data[11],data[12], data[13], data[14], 2, data[16]))
            c = "insert into moderator (Username,phone) VALUES(%s,%s) "
            mycursor.execute(c, (data[0], data[15]))
            d = "insert into moderatorqualification (QualificationID,Username,WhenAdded) VALUES(%s,%s,%s) "
            mycursor.execute(d, (data[16], data[0],now))
            con.commit()
            mycursor.close()
            con.close()
        except:  # TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("moderator input error")
            #raise RuntimeError

    def reg_admin(data):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            b = "insert into user(Username, Password, Email1, Email2, FirstName, LastName, AboutMe, PhotoURL1, PhotoURL2," \
                " PhotoURL3, StreetNumber, StreetName, MajorMunicipality, GoverningDistrict, PostalArea, UserTypeID, Status)" \
                " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(b, (
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
                data[11],data[12], data[13], data[14], 3, data[16]))
            c = "insert into administrator (Username,phone) VALUES(%s,%s) "
            mycursor.execute(c, (data[0], data[15]))
            con.commit()
            mycursor.close()
            con.close()
        except:  # TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("admin input error")