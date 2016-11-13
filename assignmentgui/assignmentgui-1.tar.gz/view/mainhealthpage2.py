import tkinter as tk
import tkinter as ttk
from tkinter import *
from model.enduser import User
from tkinter import messagebox
from controller import maincontroller

LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana",9)


# start page frame
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="You have successfully logged out!", font=MEDIUM_FONT)
        label.pack(anchor=NW, pady=10, padx=10)
        label = tk.Label(self, text="Welcome To SmartHealth", font=LARGE_FONT, fg= "Blue")
        label.pack(pady=10, padx=10)

        # show buttons
        button1 = ttk.Button(self, text="Login", command=lambda: controller.show_frame(PageLogin))
        button1.pack()
        button2 = ttk.Button(self, text="New User Register", command=lambda: controller.show_frame(PageRegister))
        button2.pack()


# login page frame
class PageLogin(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent)
        Label(self, text="Login Page", font=LARGE_FONT).grid(row=0)
        master = self
        Label(master, text="Username").grid(row=0)
        Label(master, text="Password").grid(row=1)

        self.entry1 = Entry(master)
        self.entry2 = Entry(master)

        self.entry1.grid(row=0, column=1)
        self.entry2.grid(row=1, column=1)
        Button(master, text='Quit', command=master.quit).grid(row=4, column=0, sticky=W, pady=4)
        Button(master, text='Login', command=self.show_fields).grid(row=3, column=1, sticky=W, pady=4)
        Button(master, text='Back to home', command=lambda: controlller.show_frame(StartPage)).grid(row=6, column=0,
                                                                                                    sticky=W, pady=4)

    def show_fields(self):
        s = User()
        p = self.entry1.get()
        q = self.entry2.get()
        username=s.login(p, q)
        if s.session==1:
            #root.deiconify()
            #app.pack()
            self.destroy()
            #app1=FriendshipView(username)
            #app1.mainloop()

        else:
            messagebox.showerror("Validation Error!",
                                 "You have entered invalid credentials.\n" +
                                 "Please try again.")

# class to register a user
class PageRegister(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent)
        Label(self, text="Login Page", font=LARGE_FONT)
        # label.pack(pady=10, padx=10)
        master = self
        Label(master, text="Username").grid(row=0)
        Label(master, text="Password").grid(row=1)
        Label(master, text="Email1").grid(row=2)
        Label(master, text="Email2").grid(row=3)
        Label(master, text="FirstName").grid(row=4)
        Label(master, text="LastName").grid(row=5)
        Label(master, text="AboutMe").grid(row=6)
        Label(master, text="PhotoURL1").grid(row=7)
        Label(master, text="PhotoURL2").grid(row=8)
        Label(master, text="PhotoURL3").grid(row=9)
        Label(master, text="StreetNumber").grid(row=10)
        Label(master, text="StreetName").grid(row=11)
        Label(master, text="MajorMunicipality").grid(row=12)
        Label(master, text="GoverningDistrict").grid(row=13)
        Label(master, text="PostalArea").grid(row=14)
        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        self.e4 = Entry(master)
        self.e5 = Entry(master)
        self.e6 = Entry(master)
        self.e7 = Entry(master)
        self.e8 = Entry(master)
        self.e9 = Entry(master)
        self.e10 = Entry(master)
        self.e11 = Entry(master)
        self.e12 = Entry(master)
        self.e13 = Entry(master)
        self.e14 = Entry(master)
        self.e15 = Entry(master)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        self.e5.grid(row=4, column=1)
        self.e6.grid(row=5, column=1)
        self.e7.grid(row=6, column=1)
        self.e8.grid(row=7, column=1)
        self.e9.grid(row=8, column=1)
        self.e10.grid(row=9, column=1)
        self.e11.grid(row=10, column=1)
        self.e12.grid(row=11, column=1)
        self.e13.grid(row=12, column=1)
        self.e14.grid(row=13, column=1)
        self.e15.grid(row=14, column=1)

        Button(master, text='Quit', command=master.quit).grid(row=17, column=0, sticky=W, pady=4)
        # Button(master, text='Show', command=lambda:self.show_fields()).grid(row=3, column=1, sticky=W, pady=4)
        Button(master, text='Press to Confirm', command=self.register_func).grid(row=16, column=1, sticky=W, pady=4)
        Button(master, text='Back to home', command=lambda: controlller.show_frame(StartPage)). \
            grid(row=18, column=0, sticky=W, pady=4)
        Button(self, text="Login",
               command=lambda: controlller.show_frame(PageLogin)).grid(row=17, column=1, sticky=W, pady=4)

    def register_func(self):
        username = self.e1.get()
        primary_email = self.e3.get()
        secondary_email = self.e4.get()
        password = self.e2.get()
        firstname = self.e5.get()
        lastname = self.e6.get()
        StreetNumber = self.e11.get()
        StreetName = self.e12.get()
        MajorMunicipality = self.e13.get()
        GoverningDistrict = self.e14.get()
        PostalArea = self.e15.get()
        about_user = self.e7.get()
        pic1 = self.e8.get()
        pic2 = self.e9.get()
        pic3 = self.e10.get()
        s = User()
        s.initial(username, primary_email, secondary_email, password, firstname, lastname, StreetNumber, StreetName,
                  MajorMunicipality, GoverningDistrict, PostalArea, about_user, pic1, pic2, pic3)


        # class user():
        # def initial(self,firstname,lastname,email,rollno):