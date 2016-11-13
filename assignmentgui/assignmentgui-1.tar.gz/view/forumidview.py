import tkinter as tk
from tkinter import *
from tkinter import messagebox

from controller.forumcontroller import ForumController
from model.enduser import User
from view.mainhealthpage2 import StartPage, PageLogin, PageRegister

# define text sizes and variables
from view.postview import postvvw

LARGE_FONT = ("Verdana", 12)
currentuser = ""
user_id = 0
forum_id=0
SMALL_FONT = ("Verdana", 8)
MEDIUM_FONT = ("Verdana", 10)


# class to create a forum page
class ForumV(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Smarthealth")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage1, StartPage, CreatePost, DisplayPost,DisplayPost1, PageRegister):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage1)

# method to show the frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# page to display add , display , rate the post
class StartPage1(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Forum Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        txt = "Name=" + currentuser + "   UsertypeID =" + str(user_id)+ "  Forum ID="+str(forum_id)
        label = tk.Label(self, text=txt, font=SMALL_FONT)
        label.pack(pady=15, padx=15)
        button1 = tk.Button(self, text="Display the Forum",
                            command=lambda: controlller.show_frame(DisplayPost1))
        button1.pack()
        button1 = tk.Button(self, text="ADD a Post",
                            command=lambda: controlller.show_frame(CreatePost))
        button1.pack()

        button1 = tk.Button(self, text="Display ALL Post",
                            command=lambda: controlller.show_frame(DisplayPost))
        button1.pack()


        button1 = tk.Button(self, text="Logout",
                            command=lambda: controlller.show_frame(StartPage))
        button1.pack()


# class to create post
class CreatePost(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent)
        Label(self, text="Create New Post", font=LARGE_FONT).grid(row=0)
        # label.pack(pady=10, padx=10)
        master = self

        Label(master, text="Text").grid(row=2)
        Label(master, text="p_link").grid(row=3)
        Label(master, text="v_link").grid(row=4)
        Label(master, text="link_loc").grid(row=5)
        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        self.e4 = Entry(master)
        self.e1.grid(row=2, column=1)
        self.e2.grid(row=3, column=1)
        self.e3.grid(row=4, column=1)
        self.e4.grid(row=5, column=1)




        # Button(master, text='Show', command=lambda:self.show_fields()).grid(row=3, column=1, sticky=W, pady=4)
        Button(master, text='Confirm', command=self.show_confirm).grid(row=6, column=1, sticky=W, pady=4)
        Button(master, text='Back to Forum Page', command=lambda: controlller.show_frame(StartPage1)).grid(row=9)
        Button(master, text='Quit', command=master.quit).grid(row=10)

    def show_confirm(self):
        text = self.e1.get()
        p_link= self.e2.get()
        v_link = self.e3.get()
        link_loc = self.e4.get()
        s = ForumController()
        detail = s.create_post(text, p_link, v_link, link_loc,currentuser, forum_id)
        messagebox.showinfo("Status",
                            detail)


# class to display post
class DisplayPost1(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent)
        button1 = tk.Button(self, text='Log Out', bg='#fafebe', command=lambda: controlller.show_frame(StartPage))
        button1.grid(row=0, column=8, sticky=W)

        Label(self, text="\t\t", bg='#fafebe').grid(row=0, column=1, sticky=N)
        Label(self, text="\t\t", bg='#fafebe').grid(row=0, column=5, sticky=N)
        Label(self, text="\t\t\t", bg='#fafebe').grid(row=0, column=6, sticky=N)

        label=tk.Label(self, text="Forum Details", font=LARGE_FONT)
        label.grid(row=0, column = 2)
        master = self
        s = ForumController()
        detail = s.view_forum(forum_id)
        print(detail)

        f_id = detail["ForumID"]
        topic = detail["Topic"]
        owner = detail["CreatedByModerator_Username"]
        url = detail["URL"]
        summary = detail["Summary"]

        tk.Label(self, text="Forum ID:", font=MEDIUM_FONT, bg='#fafebe').grid(row=2, column=2, sticky=W)
        tk.Label(self, text=f_id, font=MEDIUM_FONT, bg='#fafebe').grid(row=2, column=3, sticky=W)

        tk.Label(self, text="Topic:", font=MEDIUM_FONT, bg='#fafebe').grid(row=3, column=2, sticky=W)
        tk.Label(self, text=topic, font=MEDIUM_FONT, bg='#fafebe').grid(row=3, column=3, sticky=W)

        tk.Label(self, text="URL:", font=MEDIUM_FONT, bg='#fafebe').grid(row=4, column=2, sticky=W)
        tk.Label(self, text=url, font=MEDIUM_FONT, bg='#fafebe').grid(row=4, column=3, sticky=W)

        tk.Label(self, text="Summary:", font=MEDIUM_FONT, bg='#fafebe').grid(row=5, column=2, sticky=W)
        tk.Label(self, text=summary, font=MEDIUM_FONT, bg='#fafebe').grid(row=5, column=3, sticky=W)

        tk.Label(self, text="Owner name:", font=MEDIUM_FONT, bg='#fafebe').grid(row=6, column=2, sticky=W)
        tk.Label(self, text=owner, font=MEDIUM_FONT, bg='#fafebe').grid(row=6, column=3, sticky=W)

        button=tk.Button(master, text='Back to Forum Page', command=lambda: controlller.show_frame(StartPage1))
        button.grid(row=8,column=0)

class DisplayPost(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent)
        label=tk.Label(self, text="Select Post", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        s = ForumController()
        ret = s.view_post(forum_id)
        i = 0
        p = []
        q = []
        for x in ret:
            p.append(x["Username"])
            q.append(x["TimeCreated"])

        lb = tk.Listbox(self,bg='yellow',fg='blue')
        for index in enumerate(ret):
            lb.insert("end", p[i]+',' +str(q[i]))
            i = i + 1
        lb.bind("<Double-Button-1>", self.OnDouble)
        lb.pack(side="top", fill="both", expand=False)

        button1 = tk.Button(self, text="Back to home",
                            command=lambda: controlller.show_frame(StartPage1))
        button1.pack()
        button2 = tk.Button(self, text="Logout",
                            command=lambda: controlller.show_frame(StartPage))
        button2.pack()

    def show_confirm(self, p):
        postvvw(currentuser, user_id,forum_id, p)


    def OnDouble(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        self.show_confirm(value)





def forumvvw(name, userid,forumid):
    global currentuser
    global user_id
    global forum_id
    user_id = userid
    forum_id=forumid
    currentuser = name
    app2 = ForumV()
    app2.mainloop()