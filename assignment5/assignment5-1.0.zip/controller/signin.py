from model import signin
from view import user_profile
from tkinter import *

class signin_control:
    def check_signin(master,top_signin,user_detail):
        try:
            signin.signin_model.ForeignKey(1)
            user_pass=[]
            for data in user_detail:
                user_pass.append(data.get())
            fetch=signin.signin_model.query_signin(user_pass[0])
            if fetch[0]==user_pass[1]:
                user_profile.user_profile.top_user_profile(master,user_pass[0])
                top_signin.destroy()
            else:
                wrong_label = Message(top_signin, text="Wrong details entered")
                wrong_label.grid(row=5)

        except:
            wrong_label = Message(top_signin, text="Wrong details entered",font = "Helvetica 10",fg="red")
            wrong_label.grid(row=5)

