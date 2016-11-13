from tkinter import *
from controller import friendship,user_page,register,healthdata
from view import update_view,posts,health

class user_profile:
    def top_user_profile(master,username):
        top_profile = Toplevel(master)
        top_profile.title("User profile window")
        username_label=Label(top_profile, text="Welcome "+username,font = "Helvetica 12 bold")
        username_label.pack()
        blank=Label(top_profile,pady=10)
        blank.pack()

        usertype = register.register_control.get_usertype(username)
        view_btn=Button(top_profile, text="My profile",font = "Helvetica 10",padx = 25,bg="Rosy Brown",
                        command=(lambda: user_page.user_page.user_prof(master,top_profile,username)))
        view_btn.pack(fill=X,pady=2)
        update_btn = Button(top_profile, text="Update profile",font = "Helvetica 10",padx = 25,bg="Rosy Brown",
                            command=(lambda: update_view.update_view.update_page(master,top_profile,username)))
        update_btn.pack(fill=X,pady=2)
        if(usertype[0]==2):
            post = Button(top_profile, text="Forum", font="Helvetica 10", padx=25,bg="Rosy Brown",
                            command=(lambda: posts.posts.posts_top(master, top_profile, username)))
            post.pack(fill=X,pady=2)
        elif(usertype[0]==1):
            frnd_healthdata = Button(top_profile, text="Healthdata", font="Helvetica 10", padx=25, bg="Rosy Brown"
                                , command=(lambda: health.friends_healthdata.top(master, username)))
            frnd_healthdata.pack(fill=X, pady=2)
            post = Button(top_profile, text="Post / Comment / Rating", font="Helvetica 10", padx=25,bg="Rosy Brown",
                            command=(lambda: posts.posts.posts_top(master, top_profile, username)))
            post.pack(fill=X,pady=2)
            send_req=Button(top_profile, text="Send requests",font = "Helvetica 10",padx = 25,bg="Rosy Brown",
                            command=(lambda: friendship.friend_send.send_get_user(master,top_profile,username)))
            send_req.pack(fill=X,pady=2)
            accept_req = Button(top_profile, text="Accept requests",font = "Helvetica 10",padx = 25,bg="Rosy Brown",
                                command=(lambda: friendship.friend_accept.accept_top(master,top_profile,username)))
            accept_req.pack(fill=X,pady=2)
            del_req=Button(top_profile, text="Delete requests",font = "Helvetica 10",padx = 25,bg="Rosy Brown",
                           command=(lambda: friendship.friend_reject.reject_top(master,top_profile,username)))
            del_req.pack(fill=X,pady=2)
            with_req = Button(top_profile, text="Withdraw requests",font = "Helvetica 10",padx = 25,bg="Rosy Brown",
                              command=(lambda: friendship.friend_withdraw.withdraw_top(master,top_profile,username)))
            with_req.pack(fill=X,pady=2)
            unfrnd = Button(top_profile, text="Unfriend",font = "Helvetica 10",padx = 25,bg="Rosy Brown",
                            command=(lambda: friendship.friend_unfriend.unfriend_top(master,top_profile,username)))
            unfrnd.pack(fill=X,pady=2)
        del_btn = Button(top_profile, text="Delete your profile", font="Helvetica 10",padx = 25,bg="Rosy Brown",
                        command=(lambda: user_page.user_page.del_user(master,top_profile,username)))
        del_btn.pack(fill=X,pady=2)
        logout_btn=Button(top_profile, text="Logout",font = "Helvetica 10",padx = 25,bg="Rosy Brown",
                          command=top_profile.destroy)
        logout_btn.pack(fill=X,pady=2)

class user_details:
    def user_detail_page(master,top_profile,username,data):
        top_user_data=Toplevel(master,bg="white")
        top_user_data.title("User data")
        i=0
        ref=["Email1: ","Email2: ","FirstName: ","LastName: ","AboutMe: ","PhotoURL1: ","PhotoURL2: ","PhotoURL3: ","StreetNumber:"
            ,"StreetName: ","MajorMunicipality: ","GoverningDistrict: ","PostalArea: "]
        for data_this in data:
            lab=Label(top_user_data, text=str(ref[i])+ data_this,font = "Helvetica 10", bg="white")
            lab.pack(fill=X)
            i = i + 1
        ok_btn=Button(top_user_data, text="OK",font = "Helvetica 10",bg="Orchid", command=top_user_data.destroy)
        ok_btn.pack()


class friendship_class:
    def users_list(master,top_profile,usernames,username):
        send_frame=Toplevel(master)
        send_frame.title("Send Request Window")
        blank1=Label(send_frame,pady=20)
        blank1.pack(fill=X)
        user_label=Label(send_frame, text="List of usernames\n registered are: ")
        user_label.pack(fill=X)
        for user in usernames:
            user_list_label=Label(send_frame, text=user)
            user_list_label.pack(fill=X)
        blank2=Label(send_frame,pady=20)
        blank2.pack(fill=X)
        user_choice_label=Label(send_frame, text=" Enter username\n of user you want\n to add as a friend")
        user_choice_label.pack(fill=X)
        user_choice_entry=Entry(send_frame)
        user_choice_entry.pack(fill=X)
        send_frame.bind('<Return>', (lambda: friendship.friend_send.send_check_user(send_frame,username,user_choice_entry)))
        send_btn=Button(send_frame, text="Send",font = "Helvetica 10",bg="Orchid",
                        command=(lambda : friendship.friend_send.send_check_user(send_frame,username, user_choice_entry)))
        send_btn.pack(fill=X)
        back=Button(send_frame, text="Back",font = "Helvetica 10",bg="Orchid", command=send_frame.destroy)
        back.pack(fill=X)

    def accept_page(master,top_profile,usernames,username):
        top_accept=Toplevel(master)
        top_accept.title("Accept pending requests")
        usernames_lable1=Label(top_accept, text="Pending requests are:")
        usernames_lable1.pack(fill=X)
        if len(usernames)==0:
            fail_label=Label(top_accept, text="No pending requests")
            fail_label.pack(fill=X)
        else:
            usernames_lable2=Label(top_accept, text=usernames)
            usernames_lable2.pack(fill=X)
            usernames_lable3=Label(top_accept, text="Enter username of user whom you want to accept the friend request")
            usernames_lable3.pack(fill=X)
            user_entry=Entry(top_accept)
            user_entry.pack(fill=X)
            top_accept.bind('<Return>', (lambda event: friendship.friend_accept.accept_req(master,top_accept,username,user_entry)))
            accept_btn=Button(top_accept, text="Accept",font = "Helvetica 10",bg="Orchid",
                              command=(lambda: friendship.friend_accept.accept_req(master,top_accept,username,user_entry)))
            accept_btn.pack(fill=X)
        back = Button(top_accept, text="Back",font = "Helvetica 10",bg="Orchid", command=top_accept.destroy)
        back.pack(fill=X)

    def reject_page(master,top_profile,usernames,username):
        top_reject=Toplevel(master)
        top_reject.title("Reject pending requests")
        usernames_lable1=Label(top_reject, text="Pending requests are:")
        usernames_lable1.pack(fill=X)
        if len(usernames)==0:
            fail_label=Label(top_reject, text="No pending requests")
            fail_label.pack(fill=X)
        else:
            usernames_lable2=Label(top_reject, text=usernames)
            usernames_lable2.pack(fill=X)
            usernames_lable3=Label(top_reject, text="Enter username of user whom you want to reject the friend request")
            usernames_lable3.pack(fill=X)
            user_entry=Entry(top_reject)
            user_entry.pack(fill=X)
            top_reject.bind('<Return>', (lambda : friendship.friend_reject.rejet_req(master,top_reject,username,user_entry)))
            accept_btn=Button(top_reject, text="Reject",font = "Helvetica 10",bg="Orchid",
                              command=(lambda: friendship.friend_reject.reject_req(master,top_reject,username,user_entry)))
            accept_btn.pack(fill=X)
        back = Button(top_reject, text="Back",font = "Helvetica 10",bg="Orchid", command=top_reject.destroy)
        back.pack(fill=X)

    def withdraw_page(master,top_profile,usernames,username):
        top_withdraw=Toplevel(master)
        top_withdraw.title("withdraw pending requests")
        usernames_lable1=Label(top_withdraw, text="Sent requests are:")
        usernames_lable1.pack(fill=X)
        if len(usernames)==0:
            fail_label=Label(top_withdraw, text="No pending requests")
            fail_label.pack(fill=X)
        else:
            usernames_lable2=Label(top_withdraw, text=usernames)
            usernames_lable2.pack(fill=X)
            usernames_lable3=Label(top_withdraw, text="Enter username of user whom you want to withdraw the friend request")
            usernames_lable3.pack(fill=X)
            user_entry=Entry(top_withdraw)
            user_entry.pack(fill=X)
            top_withdraw.bind('<Return>', (lambda : friendship.friend_withdraw.withdraw_req(master,top_withdraw,username,user_entry)))
            accept_btn=Button(top_withdraw, text="withdraw",font = "Helvetica 10",bg="Orchid",
                              command=(lambda: friendship.friend_withdraw.withdraw_req(master,top_withdraw,username,user_entry)))
            accept_btn.pack(fill=X)
        back = Button(top_withdraw, text="Back",font = "Helvetica 10",bg="Orchid", command=top_withdraw.destroy)
        back.pack(fill=X)

    def unfriend_page(master,top_profile,usernames,usernames2,username):
        top_unfriend=Toplevel(master)
        top_unfriend.title("Unfriend")
        usernames_lable1=Label(top_unfriend, text="Friends are: ")
        usernames_lable1.pack(fill=X)
        if len(usernames)==0 and len(usernames2)==0:
            fail_label=Label(top_unfriend, text="No friends")
            fail_label.pack(fill=X)
        elif len(usernames2)==0:
            usernames_lable2=Label(top_unfriend, text=usernames)
            usernames_lable2.pack(fill=X)
            usernames_lable3=Label(top_unfriend, text="Enter username of user whom you want to unfriend the friend request")
            usernames_lable3.pack(fill=X)
            user_entry=Entry(top_unfriend)
            user_entry.pack(fill=X)
            top_unfriend.bind('<Return>', (lambda : friendship.friend_unfriend.unfriend_req(master,top_unfriend,username,user_entry)))
            accept_btn=Button(top_unfriend, text="Unfriend",font = "Helvetica 10",bg="Orchid",
                              command=(lambda: friendship.friend_unfriend.unfriend_req(master,top_unfriend,username,user_entry)))
            accept_btn.pack(fill=X)
        else:
            usernames_lable2 = Label(top_unfriend, text=usernames2)
            usernames_lable2.pack(fill=X)
            usernames_lable3 = Label(top_unfriend,
                                     text="Enter username of user whom you want to unfriend the friend request")
            usernames_lable3.pack(fill=X)
            user_entry = Entry(top_unfriend)
            user_entry.pack(fill=X)
            top_unfriend.bind('<Return>', (
            lambda: friendship.friend_unfriend.unfriend_req2(master, top_unfriend, username, user_entry)))
            accept_btn = Button(top_unfriend, text="Unfriend",font = "Helvetica 10",bg="Orchid",
                                command=(lambda: friendship.friend_unfriend.unfriend_req2(master, top_unfriend, username,
                                                                                         user_entry)))
            accept_btn.pack(fill=X)
        back = Button(top_unfriend, text="Back",font = "Helvetica 10",bg="Orchid", command=top_unfriend.destroy)
        back.pack(fill=X)
