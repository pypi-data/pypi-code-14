from tkinter import *
from controller import register

class register_view:
    def top(master):
        top_register = Toplevel(master)
        top_register.title("Registration window")
        welcome=Label(top_register, pady=30, font="Helvetica 20 bold", text="Welcome to Registration panel")
        welcome.pack(side="top")
        user=Button(top_register, padx=50, font="Helvetica 12 bold",bg="Indian Red", text="Enduser",
                    command=(lambda: register_view.reg_enduser(master,top_register)))
        user.pack(side="left")
        moder=Button(top_register, padx=50, font="Helvetica 12 bold",bg="Indian Red", text="Moderator",
                     command=(lambda: register_view.reg_moderator(master,top_register)))
        moder.pack(side="left")
        adminis=Button(top_register, padx=50, font="Helvetica 12 bold",bg="Indian Red", text="Administrator",
                       command=(lambda: register_view.reg_admin(master,top_register)))
        adminis.pack(side="left")
        close=Button(top_register, padx=50, font="Helvetica 12 bold",bg="Indian Red", text="Back",
                     command=top_register.destroy)
        close.pack(side="left")


    def make_form_enduser(top_enduser):
        username_label = Label(top_enduser, text="Enter the username: ")
        username_label.grid(row=3, column=0)
        username_entry = Entry(top_enduser)
        username_entry.grid(row=3, column=1)

        Password_label = Label(top_enduser, text="Enter the Password: ")
        Password_label.grid(row=4, column=0)
        Password_entry = Entry(top_enduser)
        Password_entry.grid(row=4, column=1)

        Email1_label = Label(top_enduser, text="Enter the Email1: ")
        Email1_label.grid(row=5, column=0)
        Email1_entry = Entry(top_enduser)
        Email1_entry.grid(row=5, column=1)

        Email2_label = Label(top_enduser, text="Enter the Email2: ")
        Email2_label.grid(row=6, column=0)
        Email2_entry = Entry(top_enduser)
        Email2_entry.grid(row=6, column=1)

        Firstname_label = Label(top_enduser, text="Enter the Firstname: ")
        Firstname_label.grid(row=7, column=0)
        Firstname_entry = Entry(top_enduser)
        Firstname_entry.grid(row=7, column=1)

        Lastname_label = Label(top_enduser, text="Enter the Lastname: ")
        Lastname_label.grid(row=8, column=0)
        Lastname_entry = Entry(top_enduser)
        Lastname_entry.grid(row=8, column=1)

        Aboutme_label = Label(top_enduser, text="Enter the Aboutme: ")
        Aboutme_label.grid(row=9, column=0)
        Aboutme_entry = Entry(top_enduser)
        Aboutme_entry.grid(row=9, column=1)

        PhotoURL1_label = Label(top_enduser, text="Enter the PhotoURL1: ")
        PhotoURL1_label.grid(row=10, column=0)
        PhotoURL1_entry = Entry(top_enduser)
        PhotoURL1_entry.grid(row=10, column=1)

        PhotoURL2_label = Label(top_enduser, text="Enter the PhotoURL2: ")
        PhotoURL2_label.grid(row=11, column=0)
        PhotoURL2_entry = Entry(top_enduser)
        PhotoURL2_entry.grid(row=11, column=1)

        PhotoURL3_label = Label(top_enduser, text="Enter the PhotoURL3: ")
        PhotoURL3_label.grid(row=12, column=0)
        PhotoURL3_entry = Entry(top_enduser)
        PhotoURL3_entry.grid(row=12, column=1)

        Streetnumber_label = Label(top_enduser, text="Enter the Streetnumber: ")
        Streetnumber_label.grid(row=13, column=0)
        Streetnumber_entry = Entry(top_enduser)
        Streetnumber_entry.grid(row=13, column=1)

        Streetname_label = Label(top_enduser, text="Enter the Streetname: ")
        Streetname_label.grid(row=14, column=0)
        Streetname_entry = Entry(top_enduser)
        Streetname_entry.grid(row=14, column=1)

        MajorMunicipality_label = Label(top_enduser, text="Enter the MajorMunicipality: ")
        MajorMunicipality_label.grid(row=15, column=0)
        MajorMunicipality_entry = Entry(top_enduser)
        MajorMunicipality_entry.grid(row=15, column=1)

        GovertricningDist_label = Label(top_enduser, text="Enter the GoverningDistrict: ")
        GovertricningDist_label.grid(row=16, column=0)
        GoverningDistrict_entry = Entry(top_enduser)
        GoverningDistrict_entry.grid(row=16, column=1)

        PostalArea_label = Label(top_enduser, text="Enter the PostalArea: ")
        PostalArea_label.grid(row=17, column=0)
        PostalArea_entry = Entry(top_enduser)
        PostalArea_entry.grid(row=17, column=1)

        data_entry = [username_entry,Password_entry,Email1_entry,Email2_entry,
                      Firstname_entry, Lastname_entry,Aboutme_entry,PhotoURL1_entry,PhotoURL2_entry,
                      PhotoURL3_entry,Streetnumber_entry,Streetname_entry,MajorMunicipality_entry,
                      GoverningDistrict_entry,PostalArea_entry]

        return data_entry

    def get_enduser(master,data_enduser,top_enduser):
        detail_enduser=[]
        for q in data_enduser:
            detail_enduser.append(q.get())
        Status = True
        detail_enduser.append(Status)
        register.register_control.cntrl_enduser(master,detail_enduser,top_enduser)

        #top_enduser.destroy()

    def reg_enduser(master,top_register):
        top_register.destroy()
        top_enduser=Toplevel(master)
        top_enduser.title("Enduser Registration panel")
        data_enduser=register_view.make_form_enduser(top_enduser)
        top_enduser.bind('<Return>', (lambda event, detail=data_enduser :register_view.get_enduser(detail,top_enduser)))
        submit = Button(top_enduser,padx=50, font="Helvetica 12 bold",bg="Sienna", text='Submit',
                        command=(lambda detail=data_enduser: register_view.get_enduser(master,detail,top_enduser)))
        submit.grid(row=18)
        back=Button(top_enduser, padx=50, font="Helvetica 12 bold",bg="Sienna", text="Back", command=top_enduser.destroy)
        back.grid(row=18, column=1)


    def make_form_moderator(top_moderator):
        username_label = Label(top_moderator, text="Enter the username: ")
        username_label.grid(row=3, column=0)
        username_entry = Entry(top_moderator)
        username_entry.grid(row=3, column=1)

        Password_label = Label(top_moderator, text="Enter the Password: ")
        Password_label.grid(row=4, column=0)
        Password_entry = Entry(top_moderator)
        Password_entry.grid(row=4, column=1)

        Email1_label = Label(top_moderator, text="Enter the Email1: ")
        Email1_label.grid(row=5, column=0)
        Email1_entry = Entry(top_moderator)
        Email1_entry.grid(row=5, column=1)

        Email2_label = Label(top_moderator, text="Enter the Email2: ")
        Email2_label.grid(row=6, column=0)
        Email2_entry = Entry(top_moderator)
        Email2_entry.grid(row=6, column=1)

        Firstname_label = Label(top_moderator, text="Enter the Firstname: ")
        Firstname_label.grid(row=7, column=0)
        Firstname_entry = Entry(top_moderator)
        Firstname_entry.grid(row=7, column=1)

        Lastname_label = Label(top_moderator, text="Enter the Lastname: ")
        Lastname_label.grid(row=8, column=0)
        Lastname_entry = Entry(top_moderator)
        Lastname_entry.grid(row=8, column=1)

        Aboutme_label = Label(top_moderator, text="Enter the Aboutme: ")
        Aboutme_label.grid(row=9, column=0)
        Aboutme_entry = Entry(top_moderator)
        Aboutme_entry.grid(row=9, column=1)

        PhotoURL1_label = Label(top_moderator, text="Enter the PhotoURL1: ")
        PhotoURL1_label.grid(row=10, column=0)
        PhotoURL1_entry = Entry(top_moderator)
        PhotoURL1_entry.grid(row=10, column=1)

        PhotoURL2_label = Label(top_moderator, text="Enter the PhotoURL2: ")
        PhotoURL2_label.grid(row=11, column=0)
        PhotoURL2_entry = Entry(top_moderator)
        PhotoURL2_entry.grid(row=11, column=1)

        PhotoURL3_label = Label(top_moderator, text="Enter the PhotoURL3: ")
        PhotoURL3_label.grid(row=12, column=0)
        PhotoURL3_entry = Entry(top_moderator)
        PhotoURL3_entry.grid(row=12, column=1)

        Streetnumber_label = Label(top_moderator, text="Enter the Streetnumber: ")
        Streetnumber_label.grid(row=13, column=0)
        Streetnumber_entry = Entry(top_moderator)
        Streetnumber_entry.grid(row=13, column=1)

        Streetname_label = Label(top_moderator, text="Enter the Streetname: ")
        Streetname_label.grid(row=14, column=0)
        Streetname_entry = Entry(top_moderator)
        Streetname_entry.grid(row=14, column=1)

        MajorMunicipality_label = Label(top_moderator, text="Enter the MajorMunicipality: ")
        MajorMunicipality_label.grid(row=15, column=0)
        MajorMunicipality_entry = Entry(top_moderator)
        MajorMunicipality_entry.grid(row=15, column=1)

        GovertricningDist_label = Label(top_moderator, text="Enter the GoverningDistrict: ")
        GovertricningDist_label.grid(row=16, column=0)
        GoverningDistrict_entry = Entry(top_moderator)
        GoverningDistrict_entry.grid(row=16, column=1)

        PostalArea_label = Label(top_moderator, text="Eer the PostalArea: ")
        PostalArea_label.grid(row=17, column=0)
        PostalArea_entry = Entry(top_moderator)
        PostalArea_entry.grid(row=17, column=1)

        PhoneNumber_label=Label(top_moderator, text="Enter your phone number: ")
        PhoneNumber_label.grid(row=18,column=0)
        PhoneNumber_entry=Entry(top_moderator)
        PhoneNumber_entry.grid(row=18,column=1)

        Qualification_label = Label(top_moderator, text="Enter your QualificationID\n(1 for M.B.B.S.,\n2 for M.D.) ")
        Qualification_label.grid(row=19, column=0)
        Qualification_entry = Entry(top_moderator)
        Qualification_entry.grid(row=19, column=1)

        data_entry = [username_entry, Password_entry, Email1_entry, Email2_entry, Aboutme_entry, PhotoURL1_entry,
                      Firstname_entry, Lastname_entry,PhotoURL2_entry,PhotoURL3_entry, Streetnumber_entry,
                      Streetname_entry, MajorMunicipality_entry,GoverningDistrict_entry, PostalArea_entry,PhoneNumber_entry
                      ,Qualification_entry]

        return data_entry

    def get_moderator(data_moderator,top_moderator):
        detail_moderator = []
        for q in data_moderator:
            detail_moderator.append(q.get())
        Status = True
        detail_moderator.append(Status)
        register.register_control.cntrl_mod(detail_moderator)
        msg=Button(top_moderator, text="Successfully\nregistered", font="Helvetica 12 bold",bg="blue",
                   command=top_moderator.destroy)
        msg.grid()

    def reg_moderator(master,top_register):
        top_register.destroy()
        top_moderator = Toplevel(master)
        top_moderator.title("Moderator Registration panel")
        data_moderator = register_view.make_form_moderator(top_moderator)
        top_moderator.bind('<Return>', (lambda event, detail=data_moderator: register_view.get_moderator(detail,top_moderator)))
        submit = Button(top_moderator, padx=50, font="Helvetica 12 bold",bg="Sienna", text='Submit',
                        command=(lambda detail=data_moderator: register_view.get_moderator(detail,top_moderator)))
        submit.grid(row=20,column=0)
        back = Button(top_moderator, padx=50, font="Helvetica 12 bold",bg="Sienna", text="Back", command=top_moderator.destroy)
        back.grid(row=20, column=1)


    def make_form_admin(top_admin):
        username_label = Label(top_admin, text="Enter the username: ")
        username_label.grid(row=3, column=0)
        username_entry = Entry(top_admin)
        username_entry.grid(row=3, column=1)

        Password_label = Label(top_admin, text="Enter the Password: ")
        Password_label.grid(row=4, column=0)
        Password_entry = Entry(top_admin)
        Password_entry.grid(row=4, column=1)

        Email1_label = Label(top_admin, text="Enter the Email1: ")
        Email1_label.grid(row=5, column=0)
        Email1_entry = Entry(top_admin)
        Email1_entry.grid(row=5, column=1)

        Email2_label = Label(top_admin, text="Enter the Email2: ")
        Email2_label.grid(row=6, column=0)
        Email2_entry = Entry(top_admin)
        Email2_entry.grid(row=6, column=1)

        Firstname_label = Label(top_admin, text="Enter the Firstname: ")
        Firstname_label.grid(row=7, column=0)
        Firstname_entry = Entry(top_admin)
        Firstname_entry.grid(row=7, column=1)

        Lastname_label = Label(top_admin, text="Enter the Lastname: ")
        Lastname_label.grid(row=8, column=0)
        Lastname_entry = Entry(top_admin)
        Lastname_entry.grid(row=8, column=1)

        Aboutme_label = Label(top_admin, text="Enter the Aboutme: ")
        Aboutme_label.grid(row=9, column=0)
        Aboutme_entry = Entry(top_admin)
        Aboutme_entry.grid(row=9, column=1)

        PhotoURL1_label = Label(top_admin, text="Enter the PhotoURL1: ")
        PhotoURL1_label.grid(row=10, column=0)
        PhotoURL1_entry = Entry(top_admin)
        PhotoURL1_entry.grid(row=10, column=1)

        PhotoURL2_label = Label(top_admin, text="Enter the PhotoURL2: ")
        PhotoURL2_label.grid(row=11, column=0)
        PhotoURL2_entry = Entry(top_admin)
        PhotoURL2_entry.grid(row=11, column=1)

        PhotoURL3_label = Label(top_admin, text="Enter the PhotoURL3: ")
        PhotoURL3_label.grid(row=12, column=0)
        PhotoURL3_entry = Entry(top_admin)
        PhotoURL3_entry.grid(row=12, column=1)

        Streetnumber_label = Label(top_admin, text="Enter the Streetnumber: ")
        Streetnumber_label.grid(row=13, column=0)
        Streetnumber_entry = Entry(top_admin)
        Streetnumber_entry.grid(row=13, column=1)

        Streetname_label = Label(top_admin, text="Enter the Streetname: ")
        Streetname_label.grid(row=14, column=0)
        Streetname_entry = Entry(top_admin)
        Streetname_entry.grid(row=14, column=1)

        MajorMunicipality_label = Label(top_admin, text="Enter the MajorMunicipality: ")
        MajorMunicipality_label.grid(row=15, column=0)
        MajorMunicipality_entry = Entry(top_admin)
        MajorMunicipality_entry.grid(row=15, column=1)

        GovertricningDist_label = Label(top_admin, text="Enter the GoverningDistrict: ")
        GovertricningDist_label.grid(row=16, column=0)
        GoverningDistrict_entry = Entry(top_admin)
        GoverningDistrict_entry.grid(row=16, column=1)

        PostalArea_label = Label(top_admin, text="Enter the PostalArea: ")
        PostalArea_label.grid(row=17, column=0)
        PostalArea_entry = Entry(top_admin)
        PostalArea_entry.grid(row=17, column=1)

        PhoneNumber_label = Label(top_admin, text="Enter your phone number: ")
        PhoneNumber_label.grid(row=18, column=0)
        PhoneNumber_entry = Entry(top_admin)
        PhoneNumber_entry.grid(row=18, column=1)

        data_entry = [username_entry, Password_entry, Email1_entry, Email2_entry,Firstname_entry,Lastname_entry,
                      Aboutme_entry,PhotoURL1_entry,PhotoURL2_entry, PhotoURL3_entry, Streetnumber_entry, Streetname_entry,
                      MajorMunicipality_entry,GoverningDistrict_entry, PostalArea_entry, PhoneNumber_entry]

        return data_entry

    def get_admin(data_admin,top_admin):
        detail_admin = []
        for q in data_admin:
            detail_admin.append(q.get())
        Status = True
        detail_admin.append(Status)
        register.register_control.cntrl_admin(detail_admin)
        msg = Button(top_admin, text="Successfully\nregistered", font="Helvetica 12 bold",bg="blue",
                     command=top_admin.destroy)
        msg.grid()

    def reg_admin(master,top_register):
        top_register.destroy()
        top_admin = Toplevel(master)
        top_admin.title("Administrator Registration panel")
        data_admin = register_view.make_form_admin(top_admin)
        top_admin.bind('<Return>', (lambda event, detail=data_admin: register_view.get_admin(detail,top_admin)))
        submit = Button(top_admin, padx=60, font="Helvetica 12 bold",bg="Sienna",  text='Submit',
                        command=(lambda detail=data_admin: register_view.get_admin(detail,top_admin)))
        submit.grid(row=19)
        back = Button(top_admin, padx=60, font="Helvetica 12 bold",bg="Sienna",text="Back", command=top_admin.destroy)
        back.grid(row=19, column=1)




