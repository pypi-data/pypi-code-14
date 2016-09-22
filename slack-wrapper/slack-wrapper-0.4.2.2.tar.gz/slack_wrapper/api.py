import requests, json, time

class API():
    def __init__(self, token):
        self.TOKEN = token
        self.domain = 'https://slack.com/api/'
        self.session = requests.Session()
        self.last_request = 0 #this will be epoch time

    def has_error(self, response_dict, log="An error ocurred:"):
        if response_dict['ok']:
            return False
        else:
            print(log)
            print(response_dict['error'])
            return True

    def api_method(self, method, extra_params={}):
        """executes any method and returns a dictionary
           this class should make all the requests because
           it takes into account Slack API's time limit
        """
        params = {'token': self.TOKEN}
        params.update(extra_params)
        if int(time.time()) - self.last_request > 1:
            pass
        else:
            time.sleep(1)
        response_dict = self.session.get(
            self.domain + method,
            params=params
        ).json()
        self.last_request = int(time.time())
        return response_dict

    def get_channel_list(self):
        """returns updated channel list"""
        response_dict = self.api_method('channels.list')
        if not self.has_error(response_dict, log='Error getting channel list:'):
            return response_dict['channels']
        else: return None

    def get_channel_name(self, channel_id):
        """returns the channel name when given an id"""
        self.channel_list = self.get_channel_list()
        for channel in self.channel_list:
            if channel["id"] == channel_id:
                return channel["name"]

    def get_channel_id(self, channel_name):
        """returns the channel id when given a name"""
        self.channel_list = self.get_channel_list()
        for channel in self.channel_list:
            if channel["name"] == channel_name:
                return channel["id"]

    def get_user_list(self):
        """returns updated user list"""
        response_dict = self.api_method('users.list')
        if not self.has_error(response_dict, log='Error getting user list:'):
            self.user_list = response_dict['members']
            return self.user_list
        else: return None

    def get_user_info(self, user_id):
        response_dict = self.api_method('users.info', {'user': user_id})
        if not self.has_error(response_dict, log='Error getting user info'):
            return response_dict['user']
        else: return None

    def get_user_id(self, username):
        self.user_list = self.get_user_list()
        for user in self.user_list:
            if user['name'] == username:
                return user['id']

    def get_user_name(self, user_id):
        user = self.get_user_info(user_id)
        if user:
            return user['name']
        else: return user

    def get_user_email(self, user_id):
        user = self.get_user_info(user_id)
        if user:
            return user['profile'].get('email', '')
        else: return user
    
    def get_groups_list(self):
        response_dict = self.api_method('groups.list', extra_params={'exclude_archived': 1})
        if not self.has_error(response_dict, log='Error getting groups list:'):
            return response_dict['groups']
        else: return None

    def get_group_id(self, group_name):
        self.groups_list = self.get_groups_list()
        for group in self.groups_list:
            if group['name'] == group_name:
                return group['id']

