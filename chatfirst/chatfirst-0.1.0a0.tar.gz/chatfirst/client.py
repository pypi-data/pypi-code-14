from chatfirst import ChatfirstClient
from chatfirst.models import Bot, Channel, ActionResponse


class Chatfirst:
    def __init__(self, token):
        self.token = token
        self.client = ChatfirstClient(token, secure=True)

    def bots_list(self):
        """
        Lists all user bots
        :return:
        """
        data = self.client.bots()
        return [Bot(item) for item in data]

    def bots_create(self, bot):
        """
        Saves new bot
        :param usertoken: User token
        :param bot: Bot object to save
        :return:
        """
        self.client.bots(_method="POST", _json=bot.to_json(), _params=dict(userToken=self.token))

    def bots_get(self, bot):
        """
        Gets bot by name
        :param bot_name: Name of Bot to fetch
        :return:
        """
        data = self.client.bots.__getattr__(bot.name).__call__()
        return Bot(data)

    def bots_update(self, bot):
        """
        Updates existing bot
        :param bot: Bot object to update
        :return:
        """
        self.client.bots.__getattr__(bot.name).__call__(_method="PUT", _json=bot.to_json(), _params=dict(botName=bot.name))

    def bots_delete(self, bot):
        """
        Deletes existing bot
        :param bot_name: Name of Bot to delete
        :return:
        """
        self.client.bots.__getattr__(bot.name).__call__(_method="DELETE", _params=dict(botName=bot.name))

    def channels_link(self, bot, channel, channel_type):
        params = dict()
        params["channel"] = channel_type
        params["externalToken"] = channel.token
        params["botName"] = bot.name
        self.client.channels.link(_method="PUT", _params=params)

    def channels_unlink(self, bot, channel_type):
        params = dict()
        params["channel"] = channel_type
        params["botName"] = bot.name
        self.client.channels.unlink(_method="PUT", _params=params)

    def channels_force(self, bot, channel_type, state):
        self.client.channels.force.__getattr__(bot.name).__getattr__(channel_type).__call__(_method="PUT", _params=dict(state=state))

    def channels_get(self, bot, channel_type):
        data = self.client.channels(_method="GET", _params=dict(channel=channel_type, botName=bot.name))
        return Channel(data)

    def talk(self, bot, message):
        data = self.client.talk(_method="POST", _params=dict(botName=bot.name), _json=message.to_json())
        return ActionResponse(data)

    def push(self, bot, channel_type, ar, user_id):
        self.client.push.__getattr__(bot.name).__call__(_method="POST",
                                                        _params=dict(id=user_id, channel=channel_type),
                                                        _json=ar.to_json())

    def broadcast(self, bot, channel_type, text):
        self.client.broadcast.__getattr__(bot.name).__call__(_method="POST",
                                                        _params=dict(channel=channel_type),
                                                        _json=dict(message=text))
