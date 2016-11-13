import tkinter as tk
from tkinter import *
from tkinter import messagebox

from controller.friendshipcontroller import FriendController
from controller.healthcontroller import HealthController
from model.enduser import User
from view.mainhealthpage2 import StartPage,PageLogin,PageRegister
#deine the font sizes
LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)
currentuser = ""
userid = 0


# class to create heath view
class HealthView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Smarthealth")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage1,StartPage,PageLogin, PageRegister,PageInsertHealth,PageDisplayHealth,PageFriendHealth):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage1)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# class for start page
class StartPage1(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent,bg='#cfffae')
        label = tk.Label(self, text="Health Page", font=LARGE_FONT,bg='#cfffae',fg='#567abc')
        label.pack(pady=10, padx=10)
        txt = "Name=" + currentuser + "   UsertypeID =" + str(userid)
        label = tk.Label(self, text=txt, font=SMALL_FONT,bg='#cfffae',fg='#567abc')
        label.pack(pady=15, padx=15)
        if userid >2:
            button1 = tk.Button(self, text="Insert Health Info",bg='#cfffae',fg='#567abc',
                            command=lambda: controlller.show_frame(PageInsertHealth))
            button1.pack()
            button2 = tk.Button(self, text="Display My Health",bg='#cfffae',fg='#567abc',
                            command=lambda: controlller.show_frame(PageDisplayHealth))
            button2.pack()
            button1 = tk.Button(self, text="Display Friend Health",bg='#cfffae',fg='#567abc',
                            command=lambda: controlller.show_frame(PageFriendHealth))
            button1.pack()
            button1 = tk.Button(self, text="Logout",bg='#cfffae',fg='#567abc',
                            command=lambda: controlller.show_frame(StartPage))
            button1.pack()
        else:
            label = tk.Label(self, text="YOU ARE NOT A USER", font=SMALL_FONT)
            label.pack(pady=15, padx=15)
            button1 = tk.Button(self, text="Logout",bg='#cfffae',fg='#567abc',
                                command=lambda: controlller.show_frame(StartPage))
            button1.pack()

# class to display health data
class PageDisplayHealth(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent,bg='#cfffae')
        label=tk.Label(self, text="My Health details", font=LARGE_FONT,bg='#cfffae',fg='#567abc',)
        label.pack(pady=10, padx=10)
        master = self
        s = HealthController()
        detail = s.display_health(currentuser)
        label = tk.Label(self, text=detail, font=LARGE_FONT,bg='#cfffae',fg='#567abc',)
        label.pack(pady=20, padx=20)

        button=tk.Button(master, text='Quit', bg='#cfffae',fg='#567abc',command=master.quit)
        button.pack()
        button=tk.Button(master, text='Back to Profile',bg='#cfffae',fg='#567abc', command=lambda: controlller.show_frame(StartPage1))
        button.pack()
# class to insert healthdata
class PageInsertHealth(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent,bg='#cfffae')
        label = tk.Label(self, text="NEW Health Data", font=LARGE_FONT,bg='#cfffae',fg='#567abc',)
        master=self
        Label(self, text="Property ID",bg='#cfffae',fg='#567abc',).grid(row=0)
        Label(self, text="Value",bg='#cfffae',fg='#567abc',).grid(row=1)
        Label(self, text="Datum ID",bg='#cfffae',fg='#567abc',).grid(row=2)
        self.e1 = Entry(self)
        self.e2 = Entry(self)
        self.e3 = Entry(self)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        Button(master, text='confirm', bg='#cfffae',fg='#567abc',command=self.show_confirma).grid(row=4, column=1, sticky=W, pady=4)

        Button(master, text='Quit', bg='#cfffae',fg='#567abc',command=master.quit).grid(row=5, column=1, sticky=W, pady=4)
        Button(master, text='Back to Profile',bg='#cfffae',fg='#567abc', command=lambda: controlller.show_frame(StartPage1)).grid(row=6, column=1, sticky=W, pady=4)

    def show_confirma(self):
        s = HealthController()
        p_id = self.e1.get()
        value = self.e2.get()
        datum_id=self.e3.get()
        message = s.insert_health(currentuser, p_id,value,datum_id)
        messagebox.showinfo("Request Status",
                            message)
#class to display health dat of a friend
class PageFriendHealth(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="friend health check", font=LARGE_FONT,bg='#cfffae',fg='#567abc',)
        master=self

        s = FriendController()
        ret = s.display_friend(currentuser)
        i = 0
        lb = tk.Listbox(self)
        for index in enumerate(ret):
            lb.insert("end", ret[i])
            i = i + 1
        lb.bind("<Double-Button-1>", self.OnDouble)
        lb.pack(side="top", fill="both", expand=True)
        button1 = tk.Button(self, text="Quit",bg='#cfffae',fg='#567abc',
                            command=master.quit)
        button1.pack()
        button2 = tk.Button(self, text="Back to profile",bg='#cfffae',fg='#567abc',
                            command=lambda: controlller.show_frame(StartPage1))
        button2.pack()

    def OnDouble(self, event):
        s = HealthController()
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        message = s.display_friend_health(currentuser, value)
        messagebox.showinfo("Friend Health details",
                            message)

def healthvw(name,user_id):
    global currentuser
    global userid
    userid=user_id
    currentuser = name
    app2 = HealthView()
    app2.mainloop()