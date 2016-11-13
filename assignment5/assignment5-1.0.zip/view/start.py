from tkinter import *
from view import register,signin

class top:
    def __init__(self,master):
        self.master=master
        self.welcome_page()

    def welcome_page(self):
        reg=Button(master, text="Register",padx = 50,font = "Helvetica 12 bold",bg="Firebrick",
                   command=(lambda: register.register_view.top(master)))
        reg.pack(side=LEFT, padx=25)
        sign=Button(master, text="Signin",padx = 50,font = "Helvetica 12 bold",bg="Firebrick",
                    command=(lambda: signin.signin_view.top(master)))
        sign.pack(side=LEFT, padx=25)
        sign=Button(master, text="Exit",padx = 50,font = "Helvetica 12 bold",bg="Firebrick", command=master.quit)
        sign.pack(side=LEFT, padx=25)


if __name__ == '__main__':
    master = Tk()
    master.title("Smart Health Terminal")
    logo = PhotoImage(file="../view/smarthealth.png")
    pic=Label(master, image=logo)
    pic.pack(side=TOP)
    obj=top(master)
    master.mainloop()
