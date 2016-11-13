from tkinter import *
from controller import forum_controller
from view import user_profile

class posts:
    def posts_top(master,top_profile,username):
        top_profile.destroy()
        top_posts=Toplevel(master)
        top_posts.title("Forum window")
        top_frame=Frame(top_posts)
        top_frame.pack(side=TOP)

        username_label = Label(top_frame, text="Welcome " + username, font="Helvetica 12 bold")
        username_label.pack()
        blank = Label(top_frame, pady=10)
        blank.pack()

        usertype=forum_controller.forum_control.check_usertype(username)
        if(usertype[0]==1):
            user_frame = Frame(top_posts)
            user_frame.pack(side=LEFT)
            new_btn=Button(user_frame, text="Post on a forum",font = "Helvetica 10",padx = 25,bg="Peach Puff"
                           , command=(lambda: posts.post_form(top_posts,username)))
            new_btn.pack(fill=X,pady=2)
            comment=Button(user_frame, text="Comment/Rating on a post",font = "Helvetica 10",padx = 25,bg="Peach Puff"
                           ,command=(lambda: posts.comment_form(top_posts,username)))
            comment.pack(fill=X,pady=2)
            back_btn = Button(user_frame, text="back",font = "Helvetica 10",padx = 25,bg="Peach Puff"
                              , command=(lambda: posts.back_user_profile(master,username,top_posts)))
            back_btn.pack(fill=X,pady=2)
        elif(usertype[0]==2):
            mod_frame = Frame(top_posts)
            mod_frame.pack(side=LEFT)
            start_btn=Button(mod_frame, text="Start a new forum",font = "Helvetica 10",padx = 25,bg="Peach Puff"
                             ,command=(lambda: forum.forum_form(top_posts,username)))
            start_btn.pack(fill=X,pady=2)
            start_btn=Button(mod_frame, text="Delete a new forum",font = "Helvetica 10",padx = 25,bg="Peach Puff"
                             , command=(lambda :forum.del_forum_form(top_posts,username)))
            start_btn.pack(fill=X,pady=2)
            back_btn = Button(mod_frame, text="back", command=(lambda: posts.back_user_profile(master,username,top_posts)),
                              font="Helvetica 10", padx=25, bg="Peach Puff")
            back_btn.pack(fill=X,pady=2)
        else:
            admin_frame=Frame(top_posts)
            admin_frame.pack(side=LEFT)
            msg=Message(admin_frame, text="Thanks for visiting this page\nGo back")
            msg.pack(fill=X,pady=2)
            back_btn = Button(admin_frame, text="back", font="Helvetica 10", padx=25, bg="Peach Puff"
                              , command=(lambda: posts.back_user_profile(master,username,top_posts)))
            back_btn.pack(fill=X,pady=2)

    def back_user_profile(master,username,top_posts):
        top_posts.destroy()
        user_profile.user_profile.top_user_profile(master, username)

    def post_form(top_posts,username):
        user_frame1 = Frame(top_posts)
        user_frame1.pack(side=LEFT)
        id_list=forum_controller.forum_control.get_forum_list(1)
        msg=Label(user_frame1, text="Existing ForumID's are as follows:")
        msg.pack(fill=X,pady=2)
        for i in id_list:
            forum_id_label=Label(user_frame1, text=i)
            forum_id_label.pack()
        blank_label=Label(user_frame1)
        blank_label.pack()
        forumid_label=Label(user_frame1,text="Forum id: ")
        forumid_label.pack()
        forumid_entry=Entry(user_frame1)
        forumid_entry.pack()
        text_label=Label(user_frame1, text="Post: ")
        text_label.pack()
        text_entry=Entry(user_frame1)
        text_entry.pack()
        photo_label=Label(user_frame1, text="Photo: ")
        photo_label.pack()
        photo_entry=Entry(user_frame1)
        photo_entry.pack()
        summ_label = Label(user_frame1, text="Summary: ")
        summ_label.pack()
        summ_entry = Entry(user_frame1)
        summ_entry.pack()
        video_label = Label(user_frame1, text="video: ")
        video_label.pack()
        video_entry = Entry(user_frame1)
        video_entry.pack()
        entries=[forumid_entry,text_entry,photo_entry,summ_entry,video_entry]
        submit_btn=Button(user_frame1, text="Submit",font = "Helvetica 10",padx = 25,bg="Peach Puff"
                          , command=(lambda:forum_controller.forum_control.new_post(user_frame1,username,entries)))
        submit_btn.pack()
        back_btn = Button(user_frame1, text="back",font = "Helvetica 10",padx = 25,bg="Peach Puff"
                          , command=user_frame1.destroy)
        back_btn.pack()


    def comment_form(top_posts,username):
        user_frame2 = Frame(top_posts)
        user_frame2.pack(side=LEFT)
        id_list=forum_controller.forum_control.get_forum_list(0)
        msg=Label(user_frame2, text="Existing ForumID's are as follows:")
        msg.pack(fill=X,pady=2)
        for i in id_list:
            forum_id_label=Label(user_frame2, text=i)
            forum_id_label.pack()
        blank_label=Label(user_frame2)
        blank_label.pack()
        forumid_label=Label(user_frame2,text="Forum id: ")
        forumid_label.pack()
        forumid_entry=Entry(user_frame2)
        forumid_entry.pack()
        view_posts_btn=Button(user_frame2, text="View posts for this ForumID",font = "Helvetica 10",padx = 25,bg="Peach Puff",
                              command=(lambda:forum_controller.forum_control.get_post_list(top_posts,user_frame2,forumid_entry,username)))
        view_posts_btn.pack(fill=X)
        back_btn = Button(user_frame2, text="back", font="Helvetica 10", padx=25, bg="Peach Puff"
                          , command=user_frame2.destroy)
        back_btn.pack()

    def comment_rating(top_posts,user_frame2,username,id_list,post_list,forumid_entry):
        msg=Label(user_frame2, text="Existing Usernames with Posts \nfor entered forumid are as follows:")
        msg.pack(fill=X,pady=2)
        len_id=len(id_list)
        if len_id==0:
            blank_label = Label(user_frame2, text="No Posts exist for this forum")
            blank_label.pack()
        else:
            for i in range(len_id):
                forum_id_label=Label(user_frame2, text=id_list[i] + " : " +post_list[i])
                forum_id_label.pack()
            blank_label=Label(user_frame2)
            blank_label.pack()
            comment_button=Button(user_frame2, text="Comment", font="Helvetica 10", padx=25, bg="Peach Puff",
                    command=(lambda: posts.comment(top_posts,user_frame2,username,forumid_entry)))
            comment_button.pack(fill=X)
            rating_button = Button(user_frame2, text="Rating", font="Helvetica 10", padx=25, bg="Peach Puff",
                    command=(lambda: posts.rating(top_posts,user_frame2, username,forumid_entry)))
            rating_button.pack(fill=X)
        back_btn = Button(user_frame2, text="close this window", font="Helvetica 10", padx=25, bg="Peach Puff"
                          , command=user_frame2.destroy)
        back_btn.pack()


    def comment(top_posts,user_frame2,username,forumid_entry):
        user_frame3 = Frame(top_posts)
        user_frame3.pack(side=LEFT)
        post_label=Label(user_frame3, text="Username of Post: ")
        post_label.pack()
        post_entry=Entry(user_frame3)
        post_entry.pack()
        text_label=Label(user_frame3, text="Comment: ")
        text_label.pack()
        text_entry = Entry(user_frame3)
        text_entry.pack()
        photo_label = Label(user_frame3, text="Photo: ")
        photo_label.pack()
        photo_entry = Entry(user_frame3)
        photo_entry.pack()
        link_label = Label(user_frame3, text="link: ")
        link_label.pack()
        link_entry = Entry(user_frame3)
        link_entry.pack()
        video_label = Label(user_frame3, text="video: ")
        video_label.pack()
        video_entry = Entry(user_frame3)
        video_entry.pack()
        entries = [forumid_entry, post_entry, text_entry, photo_entry, link_entry, video_entry]
        submit_btn = Button(user_frame3, text="Submit", font="Helvetica 10", padx=25, bg="Peach Puff"
                            , command=(lambda: forum_controller.forum_control.new_comment(user_frame3, username, entries)))
        submit_btn.pack()
        back_btn = Button(user_frame3, text="back",font = "Helvetica 10",padx = 25,bg="Peach Puff"
                          , command=user_frame3.destroy)
        back_btn.pack()


    def rating(top_posts,user_frame2,username,forumid_entry):
        user_frame4 = Frame(top_posts)
        user_frame4.pack(side=LEFT)
        post_label = Label(user_frame4, text="Username of Post \nyou wish to give rating: ")
        post_label.pack()
        post_entry = Entry(user_frame4)
        post_entry.pack()
        text_label = Label(user_frame4, text="Rating(out of 5): ")
        text_label.pack()
        text_entry = Entry(user_frame4)
        text_entry.pack()
        entries = [forumid_entry, post_entry, text_entry]
        submit_btn = Button(user_frame4, text="Submit", font="Helvetica 10", padx=25, bg="Peach Puff"
                            , command=(lambda: forum_controller.forum_control.new_rating(user_frame4, username, entries)))
        submit_btn.pack()
        back_btn = Button(user_frame4, text="back",font = "Helvetica 10",padx = 25,bg="Peach Puff"
                          , command=user_frame4.destroy)
        back_btn.pack()

class forum:
    def forum_form(top_posts,username):
        mod_frame1 = Frame(top_posts)
        mod_frame1.pack(side=LEFT)
        forumid_label=Label(mod_frame1,text="Unique Forum id: ")
        forumid_label.pack()
        forumid_entry=Entry(mod_frame1)
        forumid_entry.pack()
        topic_label=Label(mod_frame1, text="Topic of forum: ")
        topic_label.pack()
        topic_entry=Entry(mod_frame1)
        topic_entry.pack()
        URL_label=Label(mod_frame1, text="URL for this forum: ")
        URL_label.pack()
        URL_entry=Entry(mod_frame1)
        URL_entry.pack()
        link_label = Label(mod_frame1, text="Summary: ")
        link_label.pack()
        link_entry = Entry(mod_frame1)
        link_entry.pack()
        entries=[forumid_entry,topic_entry,URL_entry,link_entry]
        submit_btn=Button(mod_frame1, text="Submit",font = "Helvetica 10",padx = 25,bg="Peach Puff"
                          , command=(lambda:forum_controller.forum_control.new_forum(mod_frame1,username,entries)))
        submit_btn.pack()
        back_btn = Button(mod_frame1, text="back", font="Helvetica 10", padx=25, bg="Peach Puff"
                          , command=mod_frame1.destroy)
        back_btn.pack()


    def del_forum_form(top_posts,username):
        mod_frame2 = Frame(top_posts)
        mod_frame2.pack(side=LEFT)
        forumid_label=Label(mod_frame2,text="Forum id: ")
        forumid_label.pack()
        forumid_entry=Entry(mod_frame2)
        forumid_entry.pack()
        submit_btn=Button(mod_frame2, text="Submit",font = "Helvetica 10",padx = 25,bg="Peach Puff"
                          , command=(lambda:forum_controller.forum_control.del_forum(mod_frame2,username,forumid_entry)))
        submit_btn.pack()
        back_btn = Button(mod_frame2, text="back", font="Helvetica 10", padx=25, bg="Peach Puff"
                          , command=mod_frame2.destroy)
        back_btn.pack()

class msgs:
    def post_msg(top_profile):
        top_profile.destroy()
        success_frame = Toplevel()
        success_frame.title("Sucess")
        msg_success = Message(success_frame, text="Successfully posted", font="Helvetica 10")
        msg_success.pack(fill=X)
        ok_btn = Button(success_frame, text="OK", padx=30, font="Helvetica 10 bold", command=success_frame.destroy)
        ok_btn.pack(fill=X)

    def forum_msg(top_profile):
        top_profile.destroy()
        success_frame = Toplevel()
        success_frame.title("Sucess")
        msg_success = Message(success_frame, text="Successfully created a forum", font="Helvetica 10")
        msg_success.pack(fill=X)
        ok_btn = Button(success_frame, text="OK", padx=30, font="Helvetica 10 bold", command=success_frame.destroy)
        ok_btn.pack(fill=X)

    def rating_msg(top_profile):
        top_profile.destroy()
        success_frame = Toplevel()
        success_frame.title("Sucess")
        msg_success = Message(success_frame, text="Successfully rating on the post", font="Helvetica 10")
        msg_success.pack(fill=X)
        ok_btn = Button(success_frame, text="OK", padx=30, font="Helvetica 10 bold", command=success_frame.destroy)
        ok_btn.pack(fill=X)

    def del_forum_msg(top_profile):
        top_profile.destroy()
        success_frame = Toplevel()
        success_frame.title("Sucess")
        msg_success = Message(success_frame, text="Successfull deletion of forum", font="Helvetica 10")
        msg_success.pack(fill=X)
        ok_btn = Button(success_frame, text="OK", padx=30, font="Helvetica 10 bold", command=success_frame.destroy)
        ok_btn.pack(fill=X)

    def comment_msg(top_profile):
        top_profile.destroy()
        success_frame = Toplevel()
        success_frame.title("Sucess")
        msg_success = Message(success_frame, text="Successfully commented on the post", font="Helvetica 10")
        msg_success.pack(fill=X)
        ok_btn = Button(success_frame, text="OK", padx=30, font="Helvetica 10 bold", command=success_frame.destroy)
        ok_btn.pack(fill=X)