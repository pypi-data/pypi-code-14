import tkinter as tk
import tkinter as ttk
from tkinter import *
from tkinter import messagebox
from controller.profilecontroller import ProfileController
from view.mainhealthpage2 import StartPage, PageLogin, PageRegister


current_user = ""
user_id = 0

# declaring size and font to be used
LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)
MEDIUM_FONT = ("Verdana", 10)


# profile view
class ProfileView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "SmartHealth")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # for all these frames
        self.frames = {}
        for Frames in (DisplayDetail, UpdateDetailAdmin,UpdateDetailMod,UpdateDetailUser, DeactivateAccount, StartPage1,
                       StartPage, PageLogin, PageRegister):
            frame = Frames(container, self)
            self.frames[Frames] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage1)

    # show frames
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# start page
class StartPage1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#9ced9e')

        # show logout option if user wants to log out and go back to main page
        button1 = tk.Button(self, text='Log Out', command=lambda: controller.show_frame(StartPage))
        button1.pack(anchor=NE, padx=1, pady=3)

        # display Profile label
        label = tk.Label(self, text="Your Profile", font=LARGE_FONT, fg = "#555bfe",bg='#9ced9e')
        label.pack(ipady=10, ipadx=10)
        txt = "NAME -> " + current_user + "\tUSERTYPE ID -> " + str(user_id)
        label = tk.Label(self, text=txt, font=SMALL_FONT,fg = "#555bfe",bg='#9ced9e')
        label.pack(pady=15, padx=15)

        # show the choices
        button1 = ttk.Button(self, text=" View Details ", command=lambda: controller.show_frame(DisplayDetail))
        button1.pack()

        # based on user ID it will update the changes
        if user_id == 1:
            button2 = ttk.Button(self, text="Update Details", command=lambda: controller.show_frame(UpdateDetailAdmin))
            button2.pack()
        elif user_id == 2:
            button2 = ttk.Button(self, text="Update Details", command=lambda: controller.show_frame(UpdateDetailMod))
            button2.pack()
        else:
            button2 = ttk.Button(self, text="Update Details", command=lambda: controller.show_frame(UpdateDetailUser))
            button2.pack()

        # or deactivate the account
        button3 = ttk.Button(self, text="Deactivate", command=lambda: controller.show_frame(DeactivateAccount))
        button3.pack()


# display details when user select view details option
class DisplayDetail(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent,bg='#fafebe')

        # show logout option if user wants to log out and go back to main page
        button1 = tk.Button(self, text='Log Out',bg='#fafebe', command=lambda: controller.show_frame(StartPage))
        button1.grid(row=0, column=8, sticky=W)
        Label(self, text="\t\t", bg='#fafebe').grid(row=0, column=1, sticky=N)
        Label(self, text="\t\t",bg='#fafebe').grid(row=0, column=5, sticky=N)
        Label(self, text="\t\t\t",bg='#fafebe').grid(row=0, column=6, sticky=N)

        # show the details
        label = Label(self, text="Your Details",bg='#fafebe', font=LARGE_FONT)
        label.grid(row=0, column=2, sticky=N)

        master = self
        cont = ProfileController()
        detail = cont.display(current_user, user_id)

        username = detail["Username"]
        email1 = detail["Email1"]
        email2= detail["Email2"]
        f_name = detail["FirstName"]
        l_name = detail["LastName"]
        abt_me = detail["AboutMe"]
        id = detail["UserTypeID"]

        # show username
        tk.Label(self, text="Username:", font=MEDIUM_FONT,bg='#fafebe').grid(row=2, column=2, sticky=W)
        tk.Label(self, text=username, font=MEDIUM_FONT,bg='#fafebe').grid(row=2, column=3, sticky=W)

        tk.Label(self, text="Email1:", font=MEDIUM_FONT, bg='#fafebe').grid(row=3, column=2, sticky=W)
        tk.Label(self, text=email1, font=MEDIUM_FONT, bg='#fafebe').grid(row=3, column=3, sticky=W)

        tk.Label(self, text="Email2:", font=MEDIUM_FONT, bg='#fafebe').grid(row=4, column=2, sticky=W)
        tk.Label(self, text=email2, font=MEDIUM_FONT, bg='#fafebe').grid(row=4, column=3, sticky=W)

        tk.Label(self, text="First name:", font=MEDIUM_FONT, bg='#fafebe').grid(row=5, column=2, sticky=W)
        tk.Label(self, text=f_name, font=MEDIUM_FONT, bg='#fafebe').grid(row=5, column=3, sticky=W)

        tk.Label(self, text="Last name:", font=MEDIUM_FONT, bg='#fafebe').grid(row=6, column=2, sticky=W)
        tk.Label(self, text=l_name, font=MEDIUM_FONT, bg='#fafebe').grid(row=6, column=3, sticky=W)

        tk.Label(self, text="About Me:", font=MEDIUM_FONT, bg='#fafebe').grid(row=7, column=2, sticky=W)
        tk.Label(self, text=abt_me, font=MEDIUM_FONT, bg='#fafebe').grid(row=7, column=3, sticky=W)

        # show ID
        tk.Label(self, text="ID      :", font=MEDIUM_FONT,bg='#fafebe').grid(row=9, column=2, sticky=W)
        tk.Label(self, text=id, font=MEDIUM_FONT,bg='#fafebe').grid(row=9, column=3, sticky=W)

        button1 = tk.Button(self, text='Back to Profile',bg='#fafebe', command=lambda: controller.show_frame(StartPage1))
        button1.grid(row=11, column=0)


# update details specific to the administrator
class UpdateDetailAdmin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#fafebe')

        # show logout option if user wants to log out and go back to main page
        ttk.Button(self, text='Log Out', command=lambda: controller.show_frame(StartPage))\
            .grid(row=0, column=3, sticky= W, pady=4)

        # show the label update details
        tk.Label(self, text="Update Details", font=MEDIUM_FONT,fg = "#afd101",bg='#fafebe').grid(row=1, column=1, sticky=N)
        master=self

        # take the field to be update
        tk.Label(self, text="Phone Number",fg = "#afd101",bg='#fafebe').grid(row=2)
        self.entry1 = Entry(self)
        self.entry1.grid(row=2, column=1)
        ttk.Button(master, text='Confirm', command=self.show_confirma).grid(row=3, column=1, sticky = N, pady=4)
        ttk.Button(master, text='Back to Profile', command=lambda: controller.show_frame(StartPage1))\
            .grid(row=0, column=0, sticky=N, pady=4)

    # show frame of confirm details changed
    def show_confirma(self):
        cont = ProfileController()
        entry = self.entry1.get()
        message = cont.update_profilea(current_user, entry)
        messagebox.showinfo("Request Status", message)

# class to update details of Moderator
class UpdateDetailMod(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#fafebe')

        # show logout option if user wants to log out and go back to main page
        ttk.Button(self, text='Log Out', command=lambda: controller.show_frame(StartPage)) \
            .grid(row=0, column=3, sticky=W, pady=4)

        # show the label of update page
        tk.Label(self, text="Update Details", font=MEDIUM_FONT,fg = "#afd101",bg='#fafebe').grid(row=1, column=1, sticky=N)
        master=self

        # take the fields to be updated
        Label(self, text="New Phone Number").grid(row=2)
        self.entry1 = Entry(self)
        self.entry1.grid(row=2, column=1)
        Label(self, text="New Qualification").grid(row=3)
        self.entry2 = Entry(self)
        self.entry2.grid(row=3, column=1)
        ttk.Button(master, text='Confirm', command=self.show_confirmm).grid(row=5, column=1, sticky=N, pady=4)
        ttk.Button(master, text='Back to Profile', command=lambda: controller.show_frame(StartPage1))\
            .grid(row=0, column=0, sticky=W, padx=4)

    # show the frame
    def show_confirmm(self):
        cont = ProfileController()
        entry_1 = self.entry1.get()
        entry_2 = self.entry2.get()
        message = cont.update_profilem(current_user, entry_1, entry_2)
        messagebox.showinfo("Request Status", message)


# Class to update the user details
class UpdateDetailUser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#fafebe')

        # show logout option if user wants to log out and go back to main page
        button1 = ttk.Button(self, text='Log Out', command=lambda: controller.show_frame(StartPage))
        button1.pack(anchor=NE)

        # label to show the update page
        label = tk.Label(self, text="Update Details", font=MEDIUM_FONT,fg = "#afd101",bg='#fafebe')
        label.pack(anchor=CENTER, padx=10, pady=10)
        master=self
        cont = ProfileController()
        message = cont.update_profileu(current_user)
        self.output = Text(self, height=2, width=30)
        master.output.pack()
        self.output.insert(END,"The profile has been Updated")

        button1 = ttk.Button(self, text='Back to Profile', command=lambda: controller.show_frame(StartPage1))
        button1.pack(anchor=SW)


# if user wants to delete his/her account
class DeactivateAccount(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#fafebe')

        # show logout option if user wants to log out and go back to main page
        ttk.Button(self, text='Log Out', command=lambda: controller.show_frame(StartPage)) \
            .grid(row=0, column=3, sticky=W, pady=4)

        Label(self, text="Deactivate Account", font=MEDIUM_FONT,fg = "#afd101",bg='#fafebe').grid(row=1, column=1, sticky=N)
        master = self

        # take the input if user wants to delete the account
        Label(self, text="Are You Sure You want to Deactivate?",fg = "#afd101",bg='#fafebe').grid(row=2, sticky=N)
        self.entry1 = Entry(self)
        self.entry1.grid(row=2, column=1)
        ttk.Button(master, text='Confirm', command=self.show_confirm).grid(row=4, column=1, sticky=N, pady=4)
        ttk.Button(master, text='Back to Profile', command=lambda: controller.show_frame(StartPage1))\
            .grid(row=0, column=0, sticky=W)

    # show the frames
    def show_confirm(self):
        cont = ProfileController()
        choice = self.entry1.get()

        # if user selects yes
        if choice == "yes":
            message = cont.deactivate(current_user)
            messagebox.showinfo("Status", message)
        else:
            messagebox.showinfo("Status", "Account is not deactivated")


# class to make user object of profile view function and call it in loop
def profilevw(name,userid):
    global current_user
    global user_id
    user_id=userid
    current_user = name
    app2 = ProfileView()
    app2.mainloop()
