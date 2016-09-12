# Tim Whitson
# this script is for downloading posts off of Piazza
# requires "requests" package (pip install requests)
# needs: error handling
# optional: gather comments on posts

import requests, json, getpass, sys
import yaml
import os


# input your username and password for authentication, in a file
# called .piazza The format is a yaml file as follows:
#
# piazza:
#   email: <PUT YOUR EMAIL PIAZZA USES HERE>
#   password: <PUT YOUR PASSWORD PIAZZA USES HERE>


class PiazzaExtractor:
    api_url = 'https://piazza.com/logic/api'
    login_cookie = None

    def __init__(self, id=None):
        if id is None:
            self.class_id = 'irqfvh1ctrg2vt'
        else:
            self.class_id = id

    def get_login(self, filename='.piazza'):
        with open(filename, 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
            print (config)

        password = config["piazza"]["password"]
        email = config["piazza"]["email"]
        print (email, password)
        return email, password

    def login(self, email='', password=''):
        # get username and password
        email = email if email else raw_input('Enter login email: ')
        password = password if password else getpass.getpass('Enter your password')

        # login request to get cookie
        print "logging in..."
        login_data = json.dumps({'method': 'user.login',
                                 'params': {
                                     'email': email,
                                     'pass': password}})
        login = requests.post(self.api_url, data=login_data)
        self.login_cookie = login.cookies

    def get_folder_posts(self, folder):
        print "getting items from folder..."
        data = json.dumps({'method': 'network.filter_feed',
                           'params': {
                               'nid': self.class_id,
                               'filter_folder': folder,
                               'folder': '1'}})
        folder_request = requests.post(self.api_url, data=data, cookies=self.login_cookie)
        feed = json.loads(folder_request.content)['result']['feed']

        # create array of dicts from post feed
        feed_list = []

        # grabs most recent post edit w/ fields 'uid', 'created', 'subject', and 'content' and add to array
        for index, post in enumerate(feed):
            data = json.dumps({'method': 'content.get', 'params': {'cid': post['id'], 'nid': self.class_id}})
            r = requests.post(self.api_url, data=data, cookies=self.login_cookie)
            post_json = json.loads(r.content)['result']['history'][0]  # get most current edit

            # print("===========")
            # print (post_json)
            # print("===========")


            uid = post_json['uid']  # uid of poster
            created = post_json['created']  # post creation/edit date
            subject = post_json['subject']  # post subject
            content = post_json['content']  # post content (html)
            feed_list.append({'uid': uid, 'created': created, 'subject': subject, 'content': content})

            # update progress
            sys.stdout.write('\r')
            sys.stdout.write(str(index) + '/' + str(len(feed)))
            sys.stdout.flush()

        return json.dumps({'feed': feed_list})

    # save/overwrite file as 'piazza_(folder).json'
    def save_folder_posts(self, folder):
        posts = self.get_folder_posts(folder)
        print "writing file..."
        f = open('piazza_' + '_' + folder + '.json', 'w+')
        f.write(posts)
        f.close

# example:

# folder = "d1"

# piazza = PiazzaExtractor()
# email, password = piazza.get_login()
# piazza.login(email=email, password=password)
# piazza.save_folder_posts(folder)

# os.system ("cat {folder}.json | python -m json.tool".format(**locals()))
