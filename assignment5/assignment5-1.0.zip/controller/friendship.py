from model import friend
from tkinter import *
from view import user_profile,success

class friend_send:
    def send_get_user(master,top_profile,username):
        try:
            users_list=[]
            user_list=friend.friend_send.send_get_username(1)
            for name in user_list:
                if name[0] ==username:
                    z=1
                else:
                    users_list.append(name)
            user_profile.friendship_class.users_list(master,top_profile,users_list,username)
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("*****Send Username not exists*****")
            raise RuntimeError()

    def send_check_user(send_frame,username,entered_username):
        try:
            check_list=friend.friend_send.send_check_user(entered_username.get())
            if check_list==0:
                success.msgs.msg1(send_frame)
            elif(username==entered_username.get()):
                success.msgs.msg2(send_frame)
            else:
                get_check=friend.friend_send.can_send(username)
                if(get_check==0):
                    status=friend.friend_send.send_req(username,entered_username.get())
                    if(status==True):
                        success.msgs.msg3(send_frame)
                    else:
                        success.msgs.msg4(send_frame)
                else:
                    success.msgs.msg5(send_frame)
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("qweeyfcj")
            raise RuntimeError()


class friend_accept:
    def accept_top(master,top_accept,username):
        try:
            pending_users=friend.accept_friend.accept_pending(username)
            user_profile.friendship_class.accept_page(master,top_accept,pending_users,username)
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("NOqw")

    def accept_req(master,top_accept,username,user_entry):
        try:
            friend.accept_friend.accept_req(user_entry.get(),username)
            success.success.accept_msg(top_accept)
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("NOji")


class friend_reject:
    def reject_top(master,top_reject,username):
        try:
            pending_users = friend.rejetc_friend.reject_pending(username)
            user_profile.friendship_class.reject_page(master,top_reject,pending_users,username)
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("NO requests to reject")

    def reject_req(master,top_reject,username,user_entry):
        try:
            friend.rejetc_friend.reject_req(user_entry.get(),username)
            success.success.reject_msg(top_reject)
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("NOji")


class friend_withdraw:
    def withdraw_top(master,top_withdraw,username):
        try:
            sent_req=friend.withdraw_friend.withdraw_sent(username)
            user_profile.friendship_class.withdraw_page(master,top_withdraw,sent_req,username)
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            raise RuntimeError
            print("NO requests to withdraw")

    def withdraw_req(master,top_withdraw,username,user_entry):
        try:
            friend.withdraw_friend.withdraw_req(user_entry.get(),username)
            success.success.withdraw_msg(top_withdraw)
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            raise RuntimeError
            print("NOji")


class friend_unfriend:
    def unfriend_top(master,top_unfriend,username):
        try:
            unfrnd_req=friend.unfriend_friend.unfriend_it(username)
            unfrnd_req2=friend.unfriend_friend.unfriend_it2(username)
            user_profile.friendship_class.unfriend_page(master,top_unfriend,unfrnd_req,unfrnd_req2,username)
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("NO requests to unfriend")

    def unfriend_req(master,top_unfriend,username,user_entry):
        try:
            friend.unfriend_friend.unfriend_req(user_entry.get(),username)
            success.success.unfriend_msg(top_unfriend)
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("unfrnd")

    def unfriend_req2(master,top_unfriend,username,user_entry):
        try:
            friend.unfriend_friend.unfriend_req(username,user_entry.get())
            success_label=Label(top_unfriend, text="unfriended")
            success_label.pack()
        except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
            print("unfrnd")
