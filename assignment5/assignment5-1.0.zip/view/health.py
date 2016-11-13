from tkinter import *
from controller import healthdata

class friends_healthdata:
    def top(master,username):
        top_health = Toplevel(master)
        top_health.title("Healthdata window")
        username_label = Label(top_health, text="Welcome " + username, font="Helvetica 12 bold")
        username_label.grid(row=1)
        blank = Label(top_health, pady=10)
        blank.grid(row=2)
        healthdata_window = Frame(top_health,height=200,width=200)
        healthdata_window.grid(row=10)
        friends_window=Frame(top_health,height=200,width=200)
        friends_window.grid(row=10)
        blank_window=Frame(top_health,height=200,width=200)
        blank_window.grid(row=10)
        healthdata_btn = Button(top_health, text="My Healthdata", font="Helvetica 10", padx=25, bg="Rosy Brown"
                            , command=(lambda: healthdata_class.raise_frame(healthdata_window,1, username)))
        healthdata_btn.grid(row=3)
        healthdata_btn2 = Button(top_health, text="Friends Healthdata", font="Helvetica 10", padx=25, bg="Rosy Brown"
                                , command=(lambda: healthdata_class.raise_frame(friends_window,2,username)))
        healthdata_btn2.grid(row=4)
        logout_btn = Button(top_health, text="Refresh", font="Helvetica 10", padx=25, bg="Rosy Brown",
                            command=(lambda: friends_healthdata.blank_ref(master, top_health, username)))
        logout_btn.grid(row=5)
        refr_btn = Button(top_health, text="Back", font="Helvetica 10", padx=25, bg="Rosy Brown",
                          command=top_health.destroy)
        refr_btn.grid(row=6)

    def blank_ref(master,top_health,username):
        top_health.destroy()
        friends_healthdata.top(master,username)

        
class healthdata_class:
    def raise_frame(frame,window,username):
        frame.tkraise()
        if(window==1):
            healthdata_class.healthdata_form(frame,username)
        elif(window==2):
            healthdata_class.friend_health(frame,username)

    def healthdata_form(healthdata_window,username):
        bp_label=Label(healthdata_window,text="Kilometres run: ")
        bp_label.pack(fill=X)
        bp_entry=Entry(healthdata_window)
        bp_entry.pack(fill=X)
        run_label = Label(healthdata_window, text="Calories burned: ")
        run_label.pack(fill=X)
        run_entry = Entry(healthdata_window)
        run_entry.pack(fill=X)
        entries=[bp_entry,run_entry]
        submit_btn=Button(healthdata_window, text="Submit",font = "Helvetica 10",padx = 25,bg="Peach Puff"
                          , command=(lambda :healthdata.healthdata_control.healthdata(healthdata_window,username,entries)))
        submit_btn.pack(fill=X)
        Label(healthdata_window, text="             ").pack(fill=X)
        Label(healthdata_window, text="             ").pack(fill=X)
        #back_btn = Button(healthdata_window, text="Back",font = "Helvetica 10",padx = 25,bg="Peach Puff"
                          #, command=(lambda:healthdata_class.show(healthdata_window)))
        #back_btn.grid(row=5, column=2)


    def friend_health(friends_window,username):
        list_fiend=healthdata.friend_health_control.get_friends(username)
        welcome=Label(friends_window,text="     Friends are:    ")
        welcome.pack(fill=X)
        for i in list_fiend:
            list=Label(friends_window, text=i+"         ")
            list.pack(fill=X)
        Label(friends_window, text="                ").pack(fill=X)
        frnd_label=Label(friends_window,text="Enter friends name from above list:")
        frnd_label.pack(fill=X)
        frnd_entry=Entry(friends_window)
        frnd_entry.pack(fill=X)
        get_health=Button(friends_window,text="   Get health data   ",font = "Helvetica 10",padx = 25,bg="Peach Puff",
                          command=(lambda:healthdata.healthdata_control.get_healthdata(friends_window,frnd_entry)))
        get_health.pack(fill=X)

        Label(friends_window,text="             ").pack(fill=X)
        Label(friends_window,text="             ").pack(fill=X)
        Label(friends_window,text="             ").pack(fill=X)
        Label(friends_window,text="             ").pack(fill=X)

        #back_btn = Button(friends_window, text="Back", font="Helvetica 10", padx=25, bg="Peach Puff"
                       #   , command=(lambda:healthdata_class.show(friends_window)))
        #back_btn.grid(row=j)

    def print_health(friends_window,data):
        km_label=Label(friends_window,text="Kilometers run:")
        km_label.pack(fill=X)
        value_label1=Label(friends_window,text=data[0])
        value_label1.pack(fill=X)
        cal_label = Label(friends_window, text="Calories burned: ")
        cal_label.pack(fill=X)
        value_label2 = Label(friends_window, text=data[1])
        value_label2.pack(fill=X)
