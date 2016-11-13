import tkinter as tk
from tkinter import *
from tkinter import messagebox
#select Rater_username,stars from rating,post,forum where forum.forumID=post.ForumID and post.Username=rating.rater_username and forum.forumID=1 and post.Username='charul';

from controller.forumcontroller import ForumController
from model.enduser import User
from view.mainhealthpage2 import StartPage, PageLogin, PageRegister

LARGE_FONT = ("Verdana", 12)
currentuser = ""
user_id = 0
forum_id=0
SMALL_FONT = ("Verdana", 8)


# class to create a forum page
class PostV(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Smarthealth")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage1, StartPage,DisplayPost1,CommentPost,RatePost, PageRegister):
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
        txt = "Name=" + currentuser + "   UsertypeID = " + str(user_id)+ "  Forum ID= "+str(forum_id)+\
              "  Post_Creater "+post_user+ "  Date of Post"+post_date
        label = tk.Label(self, text=txt, font=SMALL_FONT)
        label.pack(pady=15, padx=15)


        button1 = tk.Button(self, text="Display The Post",
                            command=lambda: controlller.show_frame(DisplayPost1))
        button1.pack()
        button2 = tk.Button(self, text="Comment on  Post",
                            command=lambda: controlller.show_frame(CommentPost))
        button2.pack()
        button2 = tk.Button(self, text=" Rate the Post",
                            command=lambda: controlller.show_frame(RatePost))
        button2.pack()

        button1 = tk.Button(self, text="Logout",
                            command=lambda: controlller.show_frame(StartPage))
        button1.pack()


# class to create post

# class to display post
class DisplayPost1(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent)
        label=tk.Label(self, text="post display", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        master = self
        s = ForumController()
        detail = s.view_postP(forumid,post_user)
        label = tk.Label(self, text=detail, font=SMALL_FONT)
        label.pack(pady=10, padx=10)
        button=tk.Button(master, text='Quit', command=master.quit)
        button.pack()
        button=tk.Button(master, text='Back to post page', command=lambda: controlller.show_frame(StartPage1))
        button.pack()


# class to comment post
class CommentPost(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent)
        Label(self, text="Comment on a post", font=LARGE_FONT).grid(row=0)
        master = self
        s=ForumController()
        result=s.display_comment(forumid,post_user)
        Label(self, text=result, font=LARGE_FONT).grid(row=3)

        Label(master, text="comment_text").grid(row=13)
        Label(master, text="photo_location").grid(row=14)
        Label(master, text="video_location").grid(row=15)
        Label(master, text="link_location").grid(row=16)
        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        self.e4 = Entry(master)

        self.e1.grid(row=13, column=1)
        self.e2.grid(row=14, column=1)
        self.e3.grid(row=15, column=1)
        self.e4.grid(row=16, column=1)


        # Button(master, text='Show', command=lambda:self.show_fields()).grid(row=3, column=1, sticky=W, pady=4)
        Button(master, text='Confirm', command=self.show_confirm).grid(row=18, column=1, sticky=W, pady=4)
        Button(master, text='Back to Post Page', command=lambda: controlller.show_frame(StartPage1)).grid(row=20)
        Button(master, text='Quit', command=master.quit).grid(row=22)

    def show_confirm(self):

        post_username = post_user
        comment_text= self.e1.get()
        photo_location = self.e2.get()
        video_location= self.e3.get()
        link_location = self.e4.get()
        s = ForumController()
        detail = s.create_comment(post_username, currentuser, comment_text, photo_location, video_location, link_location)
        messagebox.showinfo("Status",
                            detail)


# class to rate post
class RatePost(tk.Frame):
    def __init__(self, parent, controlller):
        tk.Frame.__init__(self, parent)
        Label(self, text="Rate a Post", font=LARGE_FONT).grid(row=1)
        s = ForumController()
        result = s.display_rating(forumid, post_user)
        Label(self, text=result, font=SMALL_FONT).grid(row=3)
        # label.pack(pady=10, padx=10)
        master = self
        Label(master, text="rating").grid(row=12)
        self.e2 = Entry(master)
        self.e2.grid(row=12, column=1)
        Button(master, text='Confirm', command=self.show_confirm).grid(row=15, column=1, sticky=W, pady=4)
        Button(master, text='Back to Post Page', command=lambda: controlller.show_frame(StartPage1)).grid(row=17)
        Button(master, text='Quit', command=master.quit).grid(row=18)

    def show_confirm(self):
        post_username = post_user
        rating= self.e2.get()
        s = ForumController()
        detail = s.create_rating( post_username,currentuser, rating)
        messagebox.showinfo("Status",
                            detail)

def postvvw(name, userid,forum_id,post):
    global currentuser
    global user_id
    global post_user
    global forumid
    global post_date
    v = post.split(',')
    user_id = userid
    forumid=forum_id
    post_user=v[0]
    post_date=v[1]
    currentuser = name
    app2 = PostV()
    app2.mainloop()