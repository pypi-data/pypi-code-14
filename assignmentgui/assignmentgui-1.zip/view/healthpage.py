import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
from controller.maincontroller import login, AMRegister, UMRegister, MMRegister
from view.afterloginview import after_login

user_id = 0

# declaring fonts to be used
E_L_FONT = ("Segoe UI Black", 20)
LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)
MEDIUM_FONT = ("Verdana", 10)


# to close the gui
def closing_protocol():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()


# main class
class SmartHealth(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "SmartHealth")
        container = tk.Frame(self)

        # set the side, fill and expand fields
        container.pack(side="top", anchor= "center", fill="both", expand=True)

        # configure the rows and columns
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Frames in (StartPage, PageLogin, PageRegisterU, PageRegisterM, PageRegisterA, NewUser):
            frame = Frames(container, self)
            self.frames[Frames] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # this function will show the frames
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# start page
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#24cac0')

        # place the welcome text
        label = tk.Label(self, text="WELCOME TO SMARTHEALTH ", font=E_L_FONT, fg="#8714bd", bg='#24cac0')
        label.pack(anchor="center")

        # option 1 if user is an existing one, and wants to login
        button1 = tk.Button(self, text="Login", font=SMALL_FONT, fg="White", bg="Blue", command=lambda: controller.show_frame(PageLogin))
        button1.pack(padx=10, pady=10, ipadx=5, ipady=5)

        # option 2 if user wants to register
        button2 = tk.Button(self, text="New User Register", font=SMALL_FONT, fg="White", bg="Blue", command=lambda: controller.show_frame(NewUser))
        button2.pack(ipadx=5, ipady=5)



# login page if button1 is selected above
class PageLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#ffddaa')

        Label(self, text="Login Page", font=MEDIUM_FONT, bg='#ffddaa',fg='#248abc').grid(row=0)
        master = self

        # ask for username and password
        Label(master, text="\t\tUsername", bg='#ffddaa',fg='#248abc').grid(row=1, column=3,sticky=N, pady=10)
        Label(master, text="\t\tPassword", bg='#ffddaa',fg='#248abc').grid(row=2, column=3, sticky=N, pady=10)

        # take username entry as normal and for pwd show * instead of characters
        self.entry1 = Entry(master)
        self.entry2 = Entry(master, show="*")
        self.entry1.grid(row=1, column=4)
        self.entry2.grid(row=2, column=4)

        # adding blank spaces
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=5, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=6, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=7, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=8, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=9, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=10, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=11, sticky=N)

        # buttons to be shown on login page
        tk.Button(master, text='Quit', command=master.quit,bg='#9ced9e',fg='black').grid(row=0, column=13, sticky=N, pady=4)
        tk.Button(master, text='Login', bg='#9ced9e',fg='black', command=self.show_fields).grid(row=4, column=4, sticky=W, padx=4, pady=4)
        tk.Button(master, text='Back to Main Page', bg='#9ced9e',fg='black', command=lambda: controller.show_frame(StartPage)) \
            .grid(row=6, column=4, sticky=W, pady=4)

        # show the above mentioned fields

    def show_fields(self):
        func = login()
        user_name = self.entry1.get()
        pwd = self.entry2.get()
        username = func.logincheck(user_name, pwd)
        global current_user

        # check the conditions
        if username is not None:
            current_user = username['Username']
            global user_id
            user_id = func.usertypeid(current_user)
            app.destroy()
            after_login(current_user, user_id)

        else:
            # show error
            messagebox.showerror("LOGIN UNSUCCESSFUL!",
                                 "You have entered an invalid email ID or password.\n" +
                                 "Please try again.")

# if user wants to create a new account
class NewUser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#ffddaa')
        Label(self, text="What role would you like to select?", font=MEDIUM_FONT, bg='#ffddaa',fg='#248abc').grid(row=0)
        master = self

        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=5, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=6, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=7, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=8, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=9, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=10, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=11, sticky=N)

        # ask user if he/she wants to register as user
        tk.Button(master, text='User', bg='#ffddaa',fg='#248abc', command=lambda: controller.show_frame(PageRegisterU))\
            .grid(row=2, column=7, sticky=N, pady=4)
        # or as administrator
        tk.Button(master, text='Administrator', bg='#ffddaa',fg='#248abc', command=lambda: controller.show_frame(PageRegisterA))\
            .grid(row=3, column=7, sticky=N, pady=4)
        # or as moderator
        tk.Button(master, text='Moderator', bg='#ffddaa',fg='#248abc', command=lambda: controller.show_frame(PageRegisterM))\
            .grid(row=4, column=7, sticky=N, pady=4)

        # go back to main page if selected registration by mistake
        tk.Button(master, text='Back to Main Page', bg='#ffddaa',fg='#248abc', command=lambda: controller.show_frame(StartPage))\
            .grid(row=8, column=0, sticky=SW, pady=4)


# register page for User
class PageRegisterU(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#ffddaa')
        Label(self, text="Registration Page", font=MEDIUM_FONT, bg='#ffddaa',fg='#248abc').grid(row=0)
        master = self

        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=5, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=6, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=7, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=8, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=9, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=10, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=11, sticky=N)

        # show options to enter the details
        Label(master, text="\tUsername", bg='#ffddaa',fg='#248abc').grid(row=1, column=3)
        Label(master, text="\tPassword", bg='#ffddaa',fg='#248abc').grid(row=2, column=3)
        Label(master, text="\tEmail1", bg='#ffddaa',fg='#248abc').grid(row=3, column=3)
        Label(master, text="\tEmail2", bg='#ffddaa',fg='#248abc').grid(row=4, column=3)
        Label(master, text="\tFirstName", bg='#ffddaa',fg='#248abc').grid(row=5, column=3)
        Label(master, text="\tLastName", bg='#ffddaa',fg='#248abc').grid(row=6, column=3)
        Label(master, text="\tAboutMe", bg='#ffddaa',fg='#248abc').grid(row=7, column=3)
        Label(master, text="\tPhotoURL1", bg='#ffddaa',fg='#248abc').grid(row=8, column=3)
        Label(master, text="\tPhotoURL2", bg='#ffddaa',fg='#248abc').grid(row=9, column=3)
        Label(master, text="\tPhotoURL3", bg='#ffddaa',fg='#248abc').grid(row=10, column=3)
        Label(master, text="\tStreetNumber", bg='#ffddaa',fg='#248abc').grid(row=11, column=3)
        Label(master, text="\tStreetName", bg='#ffddaa',fg='#248abc').grid(row=12, column=3)
        Label(master, text="\tMajorMunicipality", bg='#ffddaa',fg='#248abc').grid(row=13, column=3)
        Label(master, text="\tGoverningDistrict", bg='#ffddaa',fg='#248abc').grid(row=14, column=3)
        Label(master, text="\tPostalArea", bg='#ffddaa',fg='#248abc').grid(row=15, column=3)

        # take entries
        self.entry1 = Entry(master)
        self.entry2 = Entry(master)
        self.entry3 = Entry(master)
        self.entry4 = Entry(master)
        self.entry5 = Entry(master)
        self.entry6 = Entry(master)
        self.entry7 = Entry(master)
        self.entry8 = Entry(master)
        self.entry9 = Entry(master)
        self.entry10 = Entry(master)
        self.entry11 = Entry(master)
        self.entry12 = Entry(master)
        self.entry13 = Entry(master)
        self.entry14 = Entry(master)
        self.entry15 = Entry(master)
        self.entry1.grid(row=1, column=4)
        self.entry2.grid(row=2, column=4)
        self.entry3.grid(row=3, column=4)
        self.entry4.grid(row=4, column=4)
        self.entry5.grid(row=5, column=4)
        self.entry6.grid(row=6, column=4)
        self.entry7.grid(row=7, column=4)
        self.entry8.grid(row=8, column=4)
        self.entry9.grid(row=9, column=4)
        self.entry10.grid(row=10, column=4)
        self.entry11.grid(row=11, column=4)
        self.entry12.grid(row=12, column=4)
        self.entry13.grid(row=13, column=4)
        self.entry14.grid(row=14, column=4)
        self.entry15.grid(row=15, column=4)

        # show quit, Confirm, Back to main page and Login options
        Button(master, text='Quit', bg='#ffddaa',fg='#248abc', command=master.quit).grid(row=0, column=12, sticky=E, pady=4)
        tk.Button(master, text='Confirm', bg='#ffddaa',fg='#248abc', command=self.register_func).grid(row=17, column=4, sticky=N, pady=4)
        tk.Button(master, text='Back To Main Page', bg='#ffddaa',fg='#248abc', command=lambda: controller.show_frame(StartPage)). \
            grid(row=20, column=0, sticky=W, pady=4)
        tk.Button(self, text="Login", bg='#ffddaa',fg='#248abc', command=lambda: controller.show_frame(PageLogin))\
            .grid(row=18, column=4, sticky=N, pady=4)

    # values will be passed to registration function
    def register_func(self):
        username = self.entry1.get()
        primary_email = self.entry3.get()
        secondary_email = self.entry4.get()
        password = self.entry2.get()
        firstname = self.entry5.get()
        lastname = self.entry6.get()
        StreetNumber = self.entry11.get()
        StreetName = self.entry12.get()
        MajorMunicipality = self.entry13.get()
        GoverningDistrict = self.entry14.get()
        PostalArea = self.entry15.get()
        about_user = self.entry7.get()
        pic1 = self.entry8.get()
        pic2 = self.entry9.get()
        pic3 = self.entry10.get()
        user_register = UMRegister()
        message = user_register.initial(username, primary_email, secondary_email, password, firstname, lastname,
                                        StreetNumber,StreetName,MajorMunicipality, GoverningDistrict, PostalArea,
                                        about_user, pic1, pic2, pic3)
        messagebox.showinfo("Status", message)


# registration page for administrator
class PageRegisterA(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#ffddaa')
        Label(self, text="Registration Page", font=MEDIUM_FONT, bg='#ffddaa',fg='#248abc').grid(row=0)
        master = self

        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=5, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=6, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=7, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=8, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=9, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=10, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=11, sticky=N)

        # labels to take the entry
        Label(master, text="\tUsername", bg='#ffddaa',fg='#248abc').grid(row=1, column=3)
        Label(master, text="\tPassword", bg='#ffddaa',fg='#248abc').grid(row=2, column=3)
        Label(master, text="\tEmail1", bg='#ffddaa',fg='#248abc').grid(row=3, column=3)
        Label(master, text="\tEmail2", bg='#ffddaa',fg='#248abc').grid(row=4, column=3)
        Label(master, text="\tFirstName", bg='#ffddaa',fg='#248abc').grid(row=5, column=3)
        Label(master, text="\tLastName", bg='#ffddaa',fg='#248abc').grid(row=6, column=3)
        Label(master, text="\tAboutMe", bg='#ffddaa',fg='#248abc').grid(row=7, column=3)
        Label(master, text="\tPhotoURL1", bg='#ffddaa',fg='#248abc').grid(row=8, column=3)
        Label(master, text="\tPhotoURL2", bg='#ffddaa',fg='#248abc').grid(row=9, column=3)
        Label(master, text="\tPhotoURL3", bg='#ffddaa',fg='#248abc').grid(row=10, column=3)
        Label(master, text="\tStreetNumber", bg='#ffddaa',fg='#248abc').grid(row=11, column=3)
        Label(master, text="\tStreetName", bg='#ffddaa',fg='#248abc').grid(row=12, column=3)
        Label(master, text="\tMajorMunicipality", bg='#ffddaa',fg='#248abc').grid(row=13, column=3)
        Label(master, text="\tGoverningDistrict", bg='#ffddaa',fg='#248abc').grid(row=14, column=3)
        Label(master, text="\tPostalArea", bg='#ffddaa',fg='#248abc').grid(row=15, column=3)
        Label(self, text="\tPhone no", bg='#ffddaa',fg='#248abc').grid(row=16, column=3)

        # take entry
        self.entry1 = Entry(master)
        self.entry2 = Entry(master)
        self.entry3 = Entry(master)
        self.entry4 = Entry(master)
        self.entry5 = Entry(master)
        self.entry6 = Entry(master)
        self.entry7 = Entry(master)
        self.entry8 = Entry(master)
        self.entry9 = Entry(master)
        self.entry10 = Entry(master)
        self.entry11 = Entry(master)
        self.entry12 = Entry(master)
        self.entry13 = Entry(master)
        self.entry14 = Entry(master)
        self.entry15 = Entry(master)
        self.entry16 = Entry(master)
        self.entry1.grid(row=1, column=4)
        self.entry2.grid(row=2, column=4)
        self.entry3.grid(row=3, column=4)
        self.entry4.grid(row=4, column=4)
        self.entry5.grid(row=5, column=4)
        self.entry6.grid(row=6, column=4)
        self.entry7.grid(row=7, column=4)
        self.entry8.grid(row=8, column=4)
        self.entry9.grid(row=9, column=4)
        self.entry10.grid(row=10, column=4)
        self.entry11.grid(row=11, column=4)
        self.entry12.grid(row=12, column=4)
        self.entry13.grid(row=13, column=4)
        self.entry14.grid(row=14, column=4)
        self.entry15.grid(row=15, column=4)
        self.entry16.grid(row=16, column=4)

        # show buttons for Quit, Confirm, Back to main page and Login
        Button(master, text='Quit', bg='#ffddaa',fg='#248abc', command=master.quit).grid(row=0, column=12, sticky=E, pady=4)
        tk.Button(master, text='Confirm', bg='#ffddaa',fg='#248abc', command=self.register_func).grid(row=19, column=4, sticky=N, pady=4)
        tk.Button(master, text='Back To Main Page', bg='#ffddaa',fg='#248abc',command=lambda: controller.show_frame(StartPage)). \
            grid(row=22, column=0, sticky=W, pady=4)
        tk.Button(self, text="Login", bg='#ffddaa',fg='#248abc', command=lambda: controller.show_frame(PageLogin))\
            .grid(row=20, column=4, sticky=N, pady=4)

    # values will be passed to registration function
    def register_func(self):
        username = self.entry1.get()
        primary_email = self.entry3.get()
        secondary_email = self.entry4.get()
        password = self.entry2.get()
        firstname = self.entry5.get()
        lastname = self.entry6.get()
        StreetNumber = self.entry11.get()
        StreetName = self.entry12.get()
        MajorMunicipality = self.entry13.get()
        GoverningDistrict = self.entry14.get()
        PostalArea = self.entry15.get()
        about_user = self.entry7.get()
        pic1 = self.entry8.get()
        pic2 = self.entry9.get()
        pic3 = self.entry10.get()
        phone_no = self.entry16.get()
        admin_register = AMRegister()
        message = admin_register.initial(username, primary_email, secondary_email, password, firstname, lastname,
                                         StreetNumber, StreetName,MajorMunicipality, GoverningDistrict, PostalArea,
                                         about_user, pic1, pic2, pic3, phone_no)
        messagebox.showinfo("Status",message)


# registration page for moderator
class PageRegisterM(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#ffddaa')
        Label(self, text="Registration Page", font=MEDIUM_FONT, bg='#ffddaa',fg='#248abc').grid(row=0)
        master = self

        # adding blank spaces
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=5, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=6, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=7, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=8, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=9, sticky=N)
        Label(master, text="\t\t", bg='#ffddaa',fg='#248abc').grid(row=0, column=10, sticky=N)

        # labels to take entries
        Label(master, text="\tUsername", bg='#ffddaa',fg='#248abc').grid(row=1,column=2)
        Label(master, text="\tPassword", bg='#ffddaa',fg='#248abc').grid(row=2, column=2)
        Label(master, text="\tEmail1", bg='#ffddaa',fg='#248abc').grid(row=3, column=2)
        Label(master, text="\tEmail2", bg='#ffddaa',fg='#248abc').grid(row=4, column=2)
        Label(master, text="\tFirstName", bg='#ffddaa',fg='#248abc').grid(row=5, column=2)
        Label(master, text="\tLastName", bg='#ffddaa',fg='#248abc').grid(row=6, column=2)
        Label(master, text="\t\AboutMe", bg='#ffddaa',fg='#248abc').grid(row=7, column=2)
        Label(master, text="\tPhotoURL1", bg='#ffddaa',fg='#248abc').grid(row=8, column=2)
        Label(master, text="\tPhotoURL2", bg='#ffddaa',fg='#248abc').grid(row=9, column=2)
        Label(master, text="\tPhotoURL3", bg='#ffddaa',fg='#248abc').grid(row=10, column=2)
        Label(master, text="\tStreetNumber", bg='#ffddaa',fg='#248abc').grid(row=11, column=2)
        Label(master, text="\tStreetName", bg='#ffddaa',fg='#248abc').grid(row=12, column=2)
        Label(master, text="\tMajorMunicipality", bg='#ffddaa',fg='#248abc').grid(row=13, column=2)
        Label(master, text="\tGoverningDistrict", bg='#ffddaa',fg='#248abc').grid(row=14, column=2)
        Label(master, text="\tPostalArea", bg='#ffddaa',fg='#248abc').grid(row=15, column=2)
        Label(self, text="\tPhone no", bg='#ffddaa',fg='#248abc').grid(row=16, column=2)
        Label(self, text="\tQualification", bg='#ffddaa',fg='#248abc').grid(row=17, column=2)

        # take entries
        self.entry1 = Entry(master)
        self.entry2 = Entry(master)
        self.entry3 = Entry(master)
        self.entry4 = Entry(master)
        self.entry5 = Entry(master)
        self.entry6 = Entry(master)
        self.entry7 = Entry(master)
        self.entry8 = Entry(master)
        self.entry9 = Entry(master)
        self.entry10 = Entry(master)
        self.entry11 = Entry(master)
        self.entry12 = Entry(master)
        self.entry13 = Entry(master)
        self.entry14 = Entry(master)
        self.entry15 = Entry(master)
        self.entry16 = Entry(master)
        self.entry17 = Entry(master)
        self.entry1.grid(row=1, column=3)
        self.entry2.grid(row=2, column=3)
        self.entry3.grid(row=3, column=3)
        self.entry4.grid(row=4, column=3)
        self.entry5.grid(row=5, column=3)
        self.entry6.grid(row=6, column=3)
        self.entry7.grid(row=7, column=3)
        self.entry8.grid(row=8, column=3)
        self.entry9.grid(row=9, column=3)
        self.entry10.grid(row=10, column=3)
        self.entry11.grid(row=11, column=3)
        self.entry12.grid(row=12, column=3)
        self.entry13.grid(row=13, column=3)
        self.entry14.grid(row=14, column=3)
        self.entry15.grid(row=15, column=3)
        self.entry16.grid(row=16, column=3)
        self.entry17.grid(row=17, column=3)

        # button to show Quit, back to main page, confirm and login option
        Button(master, text='Quit', command=master.quit).grid(row=0, column=12, sticky=E, pady=4)
        tk.Button(master, text='Confirm', bg='#ffddaa',fg='#248abc', command=self.register_func).grid(row=19, column=3, sticky=N, pady=4)
        tk.Button(master, text='Back To Main Page', bg='#ffddaa',fg='#248abc', command=lambda: controller.show_frame(StartPage)). \
            grid(row=22, column=0, sticky=W, pady=4)
        tk.Button(self, text="Login", bg='#ffddaa',fg='#248abc', command=lambda: controller.show_frame(PageLogin))\
            .grid(row=20, column=3, sticky=N, pady=4)

    # passing values to registration function
    def register_func(self):
        username = self.entry1.get()
        primary_email = self.entry3.get()
        secondary_email = self.entry4.get()
        password = self.entry2.get()
        firstname = self.entry5.get()
        lastname = self.entry6.get()
        StreetNumber = self.entry11.get()
        StreetName = self.entry12.get()
        MajorMunicipality = self.entry13.get()
        GoverningDistrict = self.entry14.get()
        PostalArea = self.entry15.get()
        about_user = self.entry7.get()
        pic1 = self.entry8.get()
        pic2 = self.entry9.get()
        pic3 = self.entry10.get()
        phone_no = self.entry16.get()
        qual_id = self.entry17.get()
        mod_register = MMRegister()
        message = mod_register.initial(username, primary_email, secondary_email, password, firstname, lastname,
                                       StreetNumber,StreetName,MajorMunicipality, GoverningDistrict, PostalArea,
                                       about_user, pic1, pic2, pic3, phone_no, qual_id)
        messagebox.showinfo("Status",message)

if __name__=="__main__":
    # object of SmartHealth class which call the main loop
    app = SmartHealth()
    app.mainloop()
