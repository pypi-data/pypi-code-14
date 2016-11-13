import tkinter as tk
import tkinter as ttk
from tkinter import *
from tkinter import messagebox
from controller.friendshipcontroller import FriendController
from model.enduser import User
from view.mainhealthpage2 import StartPage, PageLogin, PageRegister

current_user = "charul"
user_id = 0

# declaring fonts to be used
LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)
MEDIUM_FONT = ("Verdana", 10)


# friendship class
class FriendshipView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "SmartHealth")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # configure the rows and the column
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # what all frames it will cover
        for Frames in (SendRequest, AcceptRequest, AcceptRequest1, StartPage1, StartPage, PageLogin, Withdraw,
                        Unfriend, PageRegister, FriendList):
            frame = Frames(container, self)
            self.frames[Frames] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage1)
        print(current_user)

    # show frames on gui
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# page 1 will show, name and user type, and options of managing friendship
class StartPage1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#faed82')

        # show logout option if user wants to log out and go back to main page
        button1 = tk.Button(self, text='Log Out',bg='#cfffae',fg='#567abc', relief='solid',
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(anchor=NE, padx=1, pady=3)

        # show the friendship page
        label = tk.Label(self, text="Friendship Page", font=MEDIUM_FONT,bg='#faed82',fg='black')
        label.pack(pady=10, padx=10)
        txt = "Name=" + current_user + "\tUsertype ID =" + str(user_id)
        label = tk.Label(self, text=txt, font=SMALL_FONT,bg='#faed82',fg='black')
        label.pack(pady=15, padx=15)
        if user_id>2:
            button1 = tk.Button(self, text="Friend list",bg='#cfffae',fg='#567abc',
                                command=lambda: controller.show_frame(FriendList))
            button1.pack()
            button1 = tk.Button(self, text="Send Request",bg='#cfffae',fg='#567abc',
                                command=lambda: controller.show_frame(SendRequest))
            button1.pack()
            button2 = tk.Button(self, text="Accept Request",bg='#cfffae',fg='#567abc',
                                command=lambda: controller.show_frame(AcceptRequest))
            button2.pack()
            button1 = tk.Button(self, text="Unfriend Request",bg='#cfffae',fg='#567abc',
                                command=lambda: controller.show_frame(Unfriend))
            button1.pack()
            button1 = tk.Button(self, text="Withdraw Request",bg='#cfffae',fg='#567abc',
                                command=lambda: controller.show_frame(Withdraw))
            button1.pack()

        else:
            label = tk.Label(self, text="YOU ARE NOT A USER", font=SMALL_FONT,bg='#cfffae',fg='#567abc')
            label.pack(pady=15, padx=15)


# frame will get open when send request is selected
class SendRequest(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # show logout option if user wants to log out and go back to main page
        ttk.Button(self, text='Log Out', command=lambda: controller.show_frame(StartPage)) \
            .grid(row=0, column=3, sticky=W, pady=4)

        # show login page
        Label(self, text="Send Request", font=MEDIUM_FONT).grid(row=1, column=1, sticky=N)
        master = self
        Label(master, text="Username to which friend request to be send").grid(row=2)

        self.entry1 = Entry(master)
        self.entry1.grid(row=2, column=1)

        ttk.Button(master, text='Confirm', command=self.show_confirm).grid(row=4, column=1, sticky=W, pady=4)
        ttk.Button(master, text='Back to Friendship Page ', command=lambda: controller.show_frame(StartPage1))\
            .grid(row=0, column=0, sticky=W, pady=4)

    # confirm a request
    def show_confirm(self):
        entry = self.entry1.get()
        cont = FriendController()
        cont.username = current_user
        str = cont.send_request(current_user, entry)
        messagebox.showinfo("Request Status",str)


    # confirm a request

# accept request from a person
class AcceptRequest(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # show logout option if user wants to log out and go back to main page
        ttk.Button(self, text='Log Out', command=lambda: controller.show_frame(StartPage)) \
            .grid(row=0, column=3, sticky=W, pady=4)
        ttk.Button(self, text='Back to Friendship Page ', command=lambda: controller.show_frame(StartPage1)) \
            .grid(row=0, column=0, sticky=W, pady=4)

        # show the label
        ttk.Label(self, text="Accept Page", font=MEDIUM_FONT).grid(row=1,column=1,sticky=N)

        cont = FriendController()
        result = cont.requestaccept(current_user)

        # check if request are pending in the queue
        if result is None:
            str = "NO REQUEST PENDING"
            self.output = Text(self, height=2, width=30)
            self.output.insert(END, str)
            self.output.grid(row=3, coulmn=1, sticky=N)
        else:
            i = 0
            for index in enumerate(result):
                ttk.Button(self, text=result[i], command=lambda: controller.show_frame(AcceptRequest1)).grid(row=3+i, column=2, sticky=N)
                i += 1

                
# class to show accept request frame
class AcceptRequest1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#abcfee')

        # show logout option if user wants to log out and go back to main page
        tk.Button(self, text='Log Out', bg='#cfffae',fg='#567abc',command=lambda: controller.show_frame(StartPage)) \
            .grid(row=0, column=3, sticky=W, pady=4)
        tk.Button(self, text='Back to Friendship Page ',bg='#cfffae',fg='#567abc', command=lambda: controller.show_frame(StartPage1)) \
            .grid(row=0, column=0, sticky=W, pady=4)

        # show the login page
        Label(self, text="Login Page", font=MEDIUM_FONT,bg='#abcfee',fg='#567abc').grid(row=1, column=1, sticky=N)
        master = self

        Label(master, text="Do you want to accept the request",bg='#abcfee',fg='#567abc').grid(row=2)
        self.entry1 = Entry(master)
        self.entry1.grid(row=2, column=1)

        tk.Button(master, text='Confirm',bg='#cfffae',fg='#567abc', command=self.show_confirm).grid(row=3, column=1, sticky=N, pady=4)

    # show if confirmed frame
    def show_confirm(self):
        cont = FriendController()
        entry = self.entry1.get()
        cont.username = current_user
        message = cont.callback(current_user, entry)
        print(message)
        messagebox.showinfo("Request Status", message)


# withdraw request from a person
class Withdraw(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#abcfee')

        label = tk.Label(self, text="Double Click friend you want to withdraw ", font=MEDIUM_FONT,bg='#cfffae',fg='#567abc')
        label.pack()
        master = self
        s = FriendController()
        ret = s.display_not_frnd_yet(current_user)
        i = 0
        lb = tk.Listbox(self)
        for index in enumerate(ret):
            lb.insert("end", ret[i])
            i = i + 1
        lb.bind("<Double-Button-1>", self.OnDouble)
        lb.pack(side="top", fill="x", expand=True)
        button2 = tk.Button(self, text="Back to Friendship Page",bg='#cfffae',fg='#567abc',command=lambda: controller.show_frame(StartPage1))
        button2.pack(side="left")
        button = tk.Button(self, text='Log Out', bg='#cfffae',fg='#567abc',command=lambda: controller.show_frame(StartPage))
        button.pack(side="right")

    #  confirm frames

    def OnDouble(self, event):
        cont = FriendController()
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        message = cont.withdraw_request(current_user, value)
        messagebox.showinfo("Status",message)


# unfriend a person
class Unfriend(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#abcfee')

        # show logout option if user wants to log out and go back to main page
        label = tk.Label(self, text="Double Click friend you want to unfriend ", font=MEDIUM_FONT,bg='#abcfee',fg='#567abc')
        label.pack()
        master = self
        s = FriendController()
        ret = s.display_friend(current_user)
        i = 0
        lb = tk.Listbox(self)
        for index in enumerate(ret):
            lb.insert("end", ret[i])
            i = i + 1
        lb.bind("<Double-Button-1>", self.OnDouble)
        lb.pack(side="top", fill="x", expand=True)
        button2 = tk.Button(self, text="Back to Friendship Page",bg='#cfffae',fg='#567abc',
                             command=lambda: controller.show_frame(StartPage1))
        button2.pack(side="left")
        button = tk.Button(self, text='Log Out', bg='#cfffae',fg='#567abc',command=lambda: controller.show_frame(StartPage))
        button.pack(side="right")
    #  confirm frames

    def OnDouble(self, event):
        cont = FriendController()
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        message = cont.unfriend(current_user, value)
        messagebox.showinfo("Status",
                            message)


# Show the friendlist
class FriendList(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#abcfee')

        # show logout option if user wants to log out and go back to main page

        label=tk.Label(self, text="FriendList", font=LARGE_FONT,bg='#abcfee',fg='#567abc')
        label.pack()
        master = self
        s = FriendController()
        ret = s.display_friend(current_user)
        i = 0
        lb = tk.Listbox(self, bg='#f0e9ad' )
        for index in enumerate(ret):
            lb.insert("end", ret[i])
            i = i + 1
        #lb.bind("<Double-Button-1>", self.OnDouble)
        lb.pack(side="top", fill="x", expand=True)
        button2 = tk.Button(self, text="Back to Friendship Page",bg='#cfffae',fg='#567abc',
                            command=lambda: controller.show_frame(StartPage1))
        button2.pack(side="left")
        button=tk.Button(self, text='Log Out',bg='#cfffae',fg='#567abc', command=lambda: controller.show_frame(StartPage))
        button.pack(side="right")


# calling friendship view
def friendshipvw(name,userid):
    global current_user
    global user_id
    user_id=userid
    current_user = name
    app2 = FriendshipView()
    app2.mainloop()
