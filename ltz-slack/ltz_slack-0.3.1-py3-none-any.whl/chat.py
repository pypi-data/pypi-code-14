import slack
import slack.http_client as hc


def post_message(channel, text, **kwargs):
    """ Sends a message to a channel

    :param channel: slack channel
    :param text: slack text
    :param kwargs: slack api call keyword arguments
    :return: slack api call result
    """

    data = {
        'token': slack.api_token,
        'channel': channel,
        'text': text
    }

    for key, value in kwargs.items():
        data[key] = value

    return hc.post('chat.postMessage', data)