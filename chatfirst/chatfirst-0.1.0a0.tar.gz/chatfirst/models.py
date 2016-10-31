import json


class ActionResponse(object):
    def __init__(self, data={}):
        self.count = data['Count'] if 'Count' in data.keys() else None
        self.messages = data['Messages'] if 'Messages' in data.keys() else []
        self.forced = data['ForcedState'] if 'ForcedState' in data.keys() else None
        self.keyboard = data['ForcedKeyboard'] if 'ForcedKeyboard' in data.keys() else None
        self.entities = [LinkedEntity(item) for item in data['Entities']] if 'Entities' in data.keys() else []

    def to_json(self):
        res = dict()
        res['Count'] = self.count
        res['Messages'] = self.messages
        res['ForcedState'] = self.forced
        res['ForcedKeyboard'] = self.keyboard
        res['Entities'] = list()
        for item in self.entities:
            res['Entities'].append(item.to_json())
        return res


class ErrorResponse(ActionResponse):
    def __init__(self, message):
        ActionResponse.__init__(self)
        self.messages = [message]


class LinkedEntity:
    def __init__(self, data={}):
        self.name = data['Name'] if 'Name' in data.keys() else None
        self.desc = data['Description'] if 'Description' in data.keys() else None
        self.url = data['ImageUrl'] if 'ImageUrl' in data.keys() else None
        self.options = data['EntityOptions'] if 'EntityOptions' in data.keys() else []

    def __str__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        res = dict()
        res['Handle'] = ''
        res['Name'] = self.name
        res['ImageUrl'] = self.url
        res['Description'] = self.desc
        res["EntityOptions"] = self.options
        return res


class Bot:
    """
    Main class defining Bot entity
    """
    def __init__(self, data={}):
        self.name = data['name'] if 'name' in data.keys() else None
        self.language = data['language'] if 'language' in data.keys() else None
        self.fancy_name = data['fancy_name'] if 'fancy_name' in data.keys() else None
        self.scenario = data['scenario'] if 'scenario' in data.keys() else None

    def to_json(self):
        data = dict()
        data['name'] = self.name
        data['language'] = self.language
        data['fancy_name'] = self.fancy_name
        data['scenario'] = self.scenario
        return data

    def __eq__(self, other):
        if not self.name == other.name:
            return False
        if not self.language == other.language:
            return False
        if not self.fancy_name == other.fancy_name:
            return False
        if not self.scenario == other.scenario:
            return False
        return True


class Channel:
    """
    Main class defining Channel entity
    """
    def __init__(self, data={}):
        self.token = data['Token'] if 'Token' in data.keys() else None
        self.name = data['Name'] if 'Name' in data.keys() else None
        self.user_token = data['UserToken'] if 'UserToken' in data.keys() else None
        self.bot_name = data['BotName'] if 'BotName' in data.keys() else None

    def to_json(self):
        data = dict()
        data['Token'] = self.token
        data['Name'] = self.name
        data['UserToken'] = self.user_token
        data['BotName'] = self.bot_name
        return data

    def __eq__(self, other):
        if not type(other) == Channel:
            return False
        if not self.name == other.name:
            return False
        if not self.token == other.token:
            return False
        if not self.user_token == other.user_token:
            return False
        if not self.bot_name == other.bot_name:
            return False
        return True


class Message:
    """
    Main class defining Message entity
    """
    def __init__(self, data={}):
        self.id_ = data['InterlocutorId'] if 'InterlocutorId' in data.keys() else None
        self.text = data['Text'] if 'Text' in data.keys() else None
        self.username = data['Username'] if 'Username' in data.keys() else None
        self.first_name = data['FirstName'] if 'FirstName' in data.keys() else None
        self.last_name = data['LastName'] if 'LastName' in data.keys() else None

    def to_json(self):
        data = dict()
        data['InterlocutorId'] = self.id_
        data['Text'] = self.text
        data['Username'] = self.username
        data['FirstName'] = self.first_name
        data['LastName'] = self.last_name
        return data

    def __eq__(self, other):
        if not type(other) == Message:
            return False
        if not self.id_ == other.id_:
            return False
        if not self.text == other.text:
            return False
        if not self.username == other.username:
            return False
        if not self.first_name == other.first_name:
            return False
        if not self.last_name == other.last_name:
            return False
        return True
