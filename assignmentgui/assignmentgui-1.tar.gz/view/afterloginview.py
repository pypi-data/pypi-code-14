import tkinter as tk
import tkinter as ttk
from tkinter import *
from view.profileview import profilevw
from view.friendshipview import friendshipvw
from view.forumview import forumvw
from view.healthview import healthvw
from view.mainhealthpage2 import StartPage

# declaring the font size and style to be used
LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)
MEDIUM_FONT = ("Verdana", 10)

current_user = ""
user_id = 0


# Login view class, showing the frame for login page
class LoginView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "SmartHealth")
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # creating frame for login page
        self.frames = {}
        for Frames in (StartPage, LoginPage):
            frame = Frames(container, self)
            self.frames[Frames] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    # show the frames on the gui
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Login page class
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#eaba98')

        # to show logout option to go back to main screen
        button1 = tk.Button(self, text='Log Out', bg='#9ced9e', relief='solid', command=lambda: controller.show_frame(StartPage))
        button1.pack(anchor=NE, padx=1, pady=3)

        # to show that user has logged in and display the options available
        label = tk.Label(self, text="YOU HAVE SUCCESSFULLY LOGGED IN!!", font=MEDIUM_FONT,bg='#eaba98')
        label.pack(ipady=10, ipadx=10)
        txt="NAME -> "+current_user+ "\tUSER TYPE ID -> "+str(user_id)
        label = tk.Label(self, text=txt, font=SMALL_FONT,bg='#eaba98', fg='brown')
        label.pack(pady=15, padx=15)

        # buttons for showing the various options available
        button1 = tk.Button(self, text="Profile", bg='#9ced9e',fg='black',relief="solid", command=self.profile)
        button1.pack()
        button1 = tk.Button(self, text="Friendship",bg='#e6b8db',fg='black', relief="solid", command=self.friend)
        button1.pack()
        button2 = tk.Button(self, text="Forum",bg='#97e3ab',fg='black', relief="solid", command=self.forum)
        button2.pack()
        button2 = tk.Button(self, text="HealthData",bg='#d3b1ea',fg='black', relief="solid", command=self.health)
        button2.pack()

    # open friendship if friendship option is selected
    def friend(self):
        friendshipvw(current_user, user_id)

    # open forum if forum option is selected
    def forum(self):
        forumvw(current_user, user_id)

    # open health if health option is selected
    def health(self):
        healthvw(current_user, user_id)

    # open profile if profile option is selected
    def profile(self):
        profilevw(current_user, user_id)


# opening the page after logging in
def after_login(name,userid):
    global current_user
    global user_id
    current_user = name
    user_id = userid
    app = LoginView()
    app.mainloop()

