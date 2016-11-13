from tkinter import *

class success:
    def del_msg(master,top_profile):
        top_profile.destroy()
        success_frame = Toplevel(master)
        success_frame.title("Sucess")
        msg_success = Message(success_frame, text="Successfully deleted", font="Helvetica 10")
        msg_success.pack(fill=X)
        ok_btn = Button(success_frame, text="OK", padx=30, font="Helvetica 10 bold", command=success_frame.destroy)
        ok_btn.pack(fill=X)

    def success_msg(window):
        msg=Label(window,text="Success")
        msg.pack(fill=X)

    def accept_msg(frame):
        msg = Button(frame, text="Request Accepted", command=frame.destroy)
        msg.pack(fill=X)

    def reject_msg(frame):
        msg = Button(frame, text="Request Rejected", command=frame.destroy)
        msg.pack(fill=X)

    def withdraw_msg(frame):
        msg = Button(frame, text="Request Withdrawn", command=frame.destroy)
        msg.pack(fill=X)

    def unfriend_msg(frame):
        msg = Button(frame, text="Unfriended", command=frame.destroy)
        msg.pack(fill=X)

    def success_update(master):
        success_frame=Toplevel(master)
        success_frame.title("Sucess")
        msg_success=Message(success_frame, text="Success",font = "Helvetica 10")
        msg_success.pack(fill=X)
        ok_btn=Button(success_frame, text="OK",padx=30,font = "Helvetica 10 bold", command=success_frame.destroy)
        ok_btn.pack(fill=X)

    def login_again(master):
        success_frame=Toplevel(master)
        success_frame.title("Login again")
        msg_success=Message(success_frame, text="Login again",font = "Helvetica 10")
        msg_success.pack(fill=X)
        ok_btn=Button(success_frame, text="OK",padx=30,font = "Helvetica 10 bold", command=success_frame.destroy)
        ok_btn.pack(fill=X)

class msgs:
    def msg1(send_frame):
        fail_label = Label(send_frame, text="No such user exists")
        fail_label.pack()

    def msg2(send_frame):
        fail_label = Label(send_frame, text="You cannot send request to yourself")
        fail_label.pack()

    def msg3(send_frame):
        succes_label = Label(send_frame, text="Friend request sent")
        succes_label.pack()

    def msg4(send_frame):
        succes_label = Label(send_frame, text="Cannot send request again")
        succes_label.pack()

    def msg5(send_frame):
        fail_label = Label(send_frame, text="Permission denied")
        fail_label.pack()

class reg_msgs:
    def success(master,top_enduser):
        new=Toplevel(master)
        Label(new,text="Successfully\nregistered").pack(fill=X)
        Label(new,text="Login to continue").pack(fill=X)
        msg = Button(new, text="OK", font="Helvetica 12", bg="white",
                     command=(lambda:reg_msgs.success_next(new,top_enduser)))
        msg.pack(fill=X)

    def fail(master,top_enduser):
        new = Toplevel(master)
        Label(new,text="Username already exists").pack(fill=X)
        Label(new, text="Try again").pack(fill=X)
        msg = Button(new, text="OK", font="Helvetica 12", bg="white",
                     command=(lambda :reg_msgs.fail_next(new,top_enduser)))
        msg.pack(fill=X)

    def success_next(new,top):
        new.destroy()
        top.destroy()

    def fail_next(new,top):
        new.destroy()
        top.destroy()