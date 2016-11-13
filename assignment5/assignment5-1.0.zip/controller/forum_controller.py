from model import forum_model
from view import posts

class forum_control:
    def check_usertype(username):
        return forum_model.get_usertype(username)

    def get_forum_list(temp):
        id_list=[]
        forum_id_list=forum_model.get_forum_id()
        for data in forum_id_list:
            id_list.append(data)
        return id_list

    def get_post_list(top_posts,frame,forumid,username):
        id_list=[]
        post_entry=[]
        post_id_list=forum_model.get_post_id(forumid.get())
        post_list=forum_model.get_post_entry(forumid.get())
        if(len(post_id_list)!=0 or len(post_list)!=0):
            for data in post_id_list[0]:
                id_list.append(data)
            for data1 in post_list[0]:
                post_entry.append(data1)
        posts.posts.comment_rating(top_posts,frame,username,id_list,post_entry,forumid.get())

    def new_post(frame,username,data):
        forum_model.new_post(username,data[0].get(),data[1].get(),data[2].get(),data[3].get(),data[4].get())
        posts.msgs.post_msg(frame)

    def new_forum(frame,username,data):
        forum_model.new_forum(data[0].get(),data[1].get(),data[2].get(),data[3].get(),username)
        posts.msgs.forum_msg(frame)

    def del_forum(frame,username,forumid):
        forum_model.del_forum(forumid.get(),username)
        posts.msgs.del_forum_msg(frame)

    def new_comment(frame,username,data):
        forum_model.new_comment(username,data[0],data[1].get(),data[2].get(),data[3].get(),data[4].get(),data[5].get())
        posts.msgs.comment_msg(frame)

    def new_rating(frame,username,data):
        forum_model.new_rating(username, data[0], data[1].get(), data[2].get())
        posts.msgs.rating_msg(frame)

    def healthdata(frame,username,data):
        frame.destroy()