from tkinter import *
from controller import signin

class signin_view:
    def top(master):
        top_signin=Toplevel(master,bg="white")
        Username_label=Label(top_signin, text="Username: ",font = "Helvetica 12",bg="white")
        Username_label.grid(row=1)
        Username_entry=Entry(top_signin)
        Username_entry.grid(row=1,column=1)
        Password_label=Label(top_signin, text="Password: ",font = "Helvetica 12",bg="white")
        Password_label.grid(row=2)
        Password_entry=Entry(top_signin,show='*')
        Password_entry.grid(row=2,column=1)
        data_entry=[Username_entry,Password_entry]
        top_signin.bind('<Return>', (lambda event,
                            detail=data_entry: signin.signin_control.check_signin(master,top_signin,detail)))
        Login=Button(top_signin, padx=50,  text='Login',font = "Helvetica 12 bold",bg="Firebrick",
                     command=(lambda detail=data_entry: signin.signin_control.check_signin(master,top_signin,detail)))
        Login.grid(row=3)
        back = Button(top_signin, padx=50,  text="Back",font = "Helvetica 12 bold",bg="Firebrick",
                      command=top_signin.destroy)
        back.grid(row=3, column=1)

