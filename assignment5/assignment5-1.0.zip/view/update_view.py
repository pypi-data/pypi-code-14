from tkinter import *
from controller import update_controller

class update_view:
    def update_page(master, top_profile, username):
        top_update = Toplevel(master)
        top_update.title("Update page")
        update_controller.update_control.get_usertype(master,top_profile,top_update,username)
        back_btn = Button(top_update, text="back", command=top_update.destroy)
        back_btn.grid(row=15)


    def make_form_enduser(master,top_profile,top_update,username):
        Password_label = Label(top_update, text="Enter the Password: ")
        Password_label.grid(row=4, column=0)
        Password_entry = Entry(top_update)
        Password_entry.grid(row=4, column=1)
        Password_buttun=Button(top_update, text="update",
            command=(lambda: update_controller.update_control.update_password(master,top_profile,top_update,Password_entry,username)))
        Password_buttun.grid(row=4, column=2)


        Firstname_label = Label(top_update, text="Enter the Firstname: ")
        Firstname_label.grid(row=5, column=0)
        Firstname_entry = Entry(top_update)
        Firstname_entry.grid(row=5, column=1)
        Firstname_buttun = Button(top_update, text="update",
                                 command=(lambda: update_controller.update_control.update_FirstName(master,Firstname_entry, username)))
        Firstname_buttun.grid(row=5, column=2)

        Lastname_label = Label(top_update, text="Enter the Lastname: ")
        Lastname_label.grid(row=6, column=0)
        Lastname_entry = Entry(top_update)
        Lastname_entry.grid(row=6, column=1)
        Lastname_buttun = Button(top_update, text="update",
                                 command=(lambda: update_controller.update_control.update_LastName(master,Lastname_entry, username)))
        Lastname_buttun.grid(row=6, column=2)

        Email1_label = Label(top_update, text="Enter the Email1: ")
        Email1_label.grid(row=7, column=0)
        Email1_entry = Entry(top_update)
        Email1_entry.grid(row=7, column=1)
        Email1_buttun = Button(top_update, text="update",
                                 command=(lambda: update_controller.update_control.update_Email1(master,Email1_entry, username)))
        Email1_buttun.grid(row=7, column=2)

        Email2_label = Label(top_update, text="Enter the Email2: ")
        Email2_label.grid(row=8, column=0)
        Email2_entry = Entry(top_update)
        Email2_entry.grid(row=8, column=1)
        Email2_buttun = Button(top_update, text="update",
                                 command=(lambda: update_controller.update_control.update_Email2(master,Email2_entry, username)))
        Email2_buttun.grid(row=8, column=2)

    def make_form_moderator(master,top_profile,top_update,username):
        Password_label = Label(top_update, text="Enter the Password: ")
        Password_label.grid(row=4, column=0)
        Password_entry = Entry(top_update)
        Password_entry.grid(row=4, column=1)
        Password_buttun = Button(top_update, text="update",
                    command=(lambda: update_controller.update_control.update_password(master,top_profile,top_update,Password_entry, username)))
        Password_buttun.grid(row=4, column=2)

        Firstname_label = Label(top_update, text="Enter the Firstname: ")
        Firstname_label.grid(row=5, column=0)
        Firstname_entry = Entry(top_update)
        Firstname_entry.grid(row=5, column=1)
        Firstname_buttun = Button(top_update, text="update",
                                  command=(lambda: update_controller.update_control.update_FirstName(master,Firstname_entry, username)))
        Firstname_buttun.grid(row=5, column=2)

        Lastname_label = Label(top_update, text="Enter the Lastname: ")
        Lastname_label.grid(row=6, column=0)
        Lastname_entry = Entry(top_update)
        Lastname_entry.grid(row=6, column=1)
        Lastname_buttun = Button(top_update, text="update",
                                 command=(lambda: update_controller.update_control.update_LastName(master,Lastname_entry, username)))
        Lastname_buttun.grid(row=6, column=2)

        Email1_label = Label(top_update, text="Enter the Email1: ")
        Email1_label.grid(row=7, column=0)
        Email1_entry = Entry(top_update)
        Email1_entry.grid(row=7, column=1)
        Email1_buttun = Button(top_update, text="update",
                               command=(lambda: update_controller.update_control.update_Email1(master,Email1_entry, username)))
        Email1_buttun.grid(row=7, column=2)

        Email2_label = Label(top_update, text="Enter the Email2: ")
        Email2_label.grid(row=8, column=0)
        Email2_entry = Entry(top_update)
        Email2_entry.grid(row=8, column=1)
        Email2_buttun = Button(top_update, text="update",
                               command=(lambda: update_controller.update_control.update_Email2(master,Email2_entry, username)))
        Email2_buttun.grid(row=8, column=2)

    def make_form_admin(master,top_profile,top_update,username):
        Password_label = Label(top_update, text="Enter the Password: ")
        Password_label.grid(row=4, column=0)
        Password_entry = Entry(top_update)
        Password_entry.grid(row=4, column=1)
        Password_buttun = Button(top_update, text="update",
                    command=(lambda: update_controller.update_control.update_password(master,top_profile,top_update,Password_entry, username)))
        Password_buttun.grid(row=4, column=2)

        Firstname_label = Label(top_update, text="Enter the Firstname: ")
        Firstname_label.grid(row=5, column=0)
        Firstname_entry = Entry(top_update)
        Firstname_entry.grid(row=5, column=1)
        Firstname_buttun = Button(top_update, text="update",
                                  command=(lambda: update_controller.update_control.update_FirstName(master,Firstname_entry, username)))
        Firstname_buttun.grid(row=5, column=2)

        Lastname_label = Label(top_update, text="Enter the Lastname: ")
        Lastname_label.grid(row=6, column=0)
        Lastname_entry = Entry(top_update)
        Lastname_entry.grid(row=6, column=1)
        Lastname_buttun = Button(top_update, text="update",
                                 command=(lambda: update_controller.update_control.update_LastName(master,Lastname_entry, username)))
        Lastname_buttun.grid(row=6, column=2)

        Email1_label = Label(top_update, text="Enter the Email1: ")
        Email1_label.grid(row=7, column=0)
        Email1_entry = Entry(top_update)
        Email1_entry.grid(row=7, column=1)
        Email1_buttun = Button(top_update, text="update",
                               command=(lambda: update_controller.update_control.update_Email1(master,Email1_entry, username)))
        Email1_buttun.grid(row=7, column=2)

        Email2_label = Label(top_update, text="Enter the Email2: ")
        Email2_label.grid(row=8, column=0)
        Email2_entry = Entry(top_update)
        Email2_entry.grid(row=8, column=1)
        Email2_buttun = Button(top_update, text="update",
                               command=(lambda: update_controller.update_control.update_Email2(master,Email2_entry, username)))
        Email2_buttun.grid(row=8, column=2)