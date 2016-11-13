import tkinter as tk
from tkinter import *
from tkinter import messagebox

from controller.forumcontroller import ForumController
from model.enduser import User
from view.forumidview import forumvvw
from view.mainhealthpage2 import StartPage, PageLogin, PageRegister

LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)
currentuser = ""
user_id = 0
forum_id=0


# class to view forum details
class ForumView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Smarthealth")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage1, StartPage, CreateForum, DisplayForum, PageRegister,DeleteForum):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage1)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# class to create , delete and display forum details
class StartPage1(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent,bg='#9ee3ca')
        label = tk.Label(self, text="Forum Page", font=LARGE_FONT,bg='#9ee3ca')
        label.pack(pady=10, padx=10)
        txt = "Name=" + currentuser + "   UsertypeID =" + str(user_id)
        label = tk.Label(self, text=txt, font=SMALL_FONT, bg='#9ee3ca')
        label.pack(pady=15, padx=15)
        if user_id==2:
            button1 = tk.Button(self, text="Create Forum",
                                command=lambda: controlller.show_frame(CreateForum))
            button1.pack()
            button1 = tk.Button(self, text="Delete Forum",
                                command=lambda: controlller.show_frame(DeleteForum))
            button1.pack()

        button1 = tk.Button(self, text="Select Forum ",
                            command=lambda: controlller.show_frame(DisplayForum))
        button1.pack()

        button1 = tk.Button(self, text="Logout",
                            command=lambda: controlller.show_frame(StartPage))
        button1.pack()


# create forum
class CreateForum(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent)
        Label(self, text="Create Forum", font=LARGE_FONT).grid(row=0)
        # label.pack(pady=10, padx=10)
        master = self

        Label(master, text="Forum ID").grid(row=1)
        Label(master, text="Topic").grid(row=2)
        Label(master, text="URL").grid(row=3)
        Label(master, text="Summary").grid(row=4)
        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        self.e4 = Entry(master)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)
        self.e4.grid(row=4, column=1)

        Button(master, text='Confirm', command=self.show_confirm).grid(row=5, column=1, sticky=W, pady=4)
        Button(master, text='Back to Forum', command=lambda: controlller.show_frame(StartPage1)).grid(row=7)
        Button(master, text='Quit', command=master.quit).grid(row=8)

    def show_confirm(self):
        forum_id = self.e1.get()
        topic= self.e2.get()
        url = self.e3.get()
        summary = self.e4.get()
        s = ForumController()
        detail = s.create_forum(topic, url, summary,currentuser, forum_id)
        messagebox.showinfo("Status",
                            detail)


# delete the forum
class DeleteForum(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent)
        Label(self, text="Delete Forum", font=LARGE_FONT).grid(row=0)
        # label.pack(pady=10, padx=10)
        master = self
        Label(self, text="enter Forum id which you want to delete").grid(row=2)
        self.e1 = Entry(self)
        self.e1.grid(row=2, column=1)
        Button(master, text='confirm', command=self.show_confirm).grid(row=4, column=1, sticky=W, pady=4)
        Button(master, text='Quit', command=master.quit).grid(row=6)
        Button(master, text='Back to Forum', command=lambda: controlller.show_frame(StartPage1)).grid(row=8)

    def show_confirm(self):
        s = ForumController()
        p = self.e1.get()

        message = s.delete_forum(currentuser,p)
        messagebox.showinfo("Status",
                            message)


# display the details of forum
class DisplayForum(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent,bg='#ff8aac')
        label=tk.Label(self, text="select the forum id", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        s=ForumController()
        ret=s.view_allforum()
        i = 0
        p = []
        q=[]
        for x in ret:
            p.append(x["ForumID"])
            q.append(x["Topic"])
        lb = tk.Listbox(self,bg='#ffddaa')
        for index in enumerate(p):
            lb.insert("end", str(p[i])+', '+q[i])
            i = i + 1
        lb.bind("<Double-Button-1>", self.OnDouble)
        lb.pack(side="top", fill="both", expand=True)


        button1 = tk.Button(self, text="Back to home",
                            command=lambda: controlller.show_frame(StartPage1))
        button1.pack()
        button2 = tk.Button(self, text="Logout",
                            command=lambda: controlller.show_frame(StartPage))
        button2.pack()

    def show_confirm(self,id):
        forumvvw(currentuser,user_id,id)

    def OnDouble(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        v=value.split(',')
        self.show_confirm(v[0])


def forumvw(name, userid):
    global currentuser
    global user_id
    user_id = userid
    currentuser = name
    app2 = ForumView()
    app2.mainloop()
