from model.friendship import Friendship
global entry
LARGE_FONT = ("Verdana", 12)
from model.enduser import User

# friendship controller
class FriendController:
    # accept the request
    def requestaccept(self, name):
        self.name = name
        c = Friendship(name)
        message = c.accept()
        # print(message)
        return message

    # callback function
    def callback(self, name, i):
        global entry
        if i == "yes":
            entry = 1
        elif i == "no":
            entry = 2
        c = Friendship(name)
        message = c.acceptupdate(entry)
        return message

    # send the request
    def send_request(self, cname, name):
        s = User()
        s.start(cname)
        message = s.sendrequest(name)
        return message

    # withdraw the request
    def withdraw_request(self, cname,name):
        s = User()
        s.start((cname))
        message = s.withdrawnrequset(name)
        return message

    # unfriend a person
    def unfriend(self, cname,name):
        s = User()
        s.start(cname)
        message = s.un_friend(name)
        return message

    # display friend list
    def display_friend(self, name):
        c = Friendship(name)
        message = c.display_friend()
        return message

    # Display list of people to whom we have sent the request
    def display_not_frnd_yet(self, name):
        c = Friendship(name)
        message = c.display_not_frnd_yet()
        return message

    # display the users available to send a request
    def display_users(self):
        s = User()
        list = s.display_users()
        return list