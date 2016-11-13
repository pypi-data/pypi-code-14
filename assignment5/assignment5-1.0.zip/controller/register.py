import pymysql
from model import register
from view import success

class register_control:
    def get_usertype(username):
        try:
            con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
            mycursor = con.cursor()
            mycursor.execute("Select UserTypeID from User WHERE Username=%s and Status=1",username)
            idtype = mycursor.fetchone()
            mycursor.close()
            con.close()
            return idtype
        except:  # TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("iderror")

    def cntrl_enduser(master,data,top_enduser):
        chk=register.register_model.check_name(data[0])
        if chk==True:
            register.register_model.reg_enduser(data)
            success.reg_msgs.success(master,top_enduser)
        else:
            success.reg_msgs.fail(master,top_enduser)

    def cntrl_mod(data):
        register.register_model.reg_mod(data)

    def cntrl_admin(data):
        register.register_model.reg_admin(data)