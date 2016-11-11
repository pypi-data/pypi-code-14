import requests
import json
import slack


def get(method, params=None):
    """ Call the Slack Web API

    Documented here: https://api.slack.com/web

    :param method: slack api call method
    :param params: slack api call keyword arguments
    :return: json response
    """
    url = _build_url(method)
    response = requests.get(url, params=params)
    return _parse_response(response)


def post(method, params=None):
    """ Call the Slack Web API by Post Method

    :param method: slack api call method
    :param params: slack api call keyword arguments
    :return: json response
    """
    url = _build_url(method)
    response = requests.post(url, params=params)
    return _parse_response(response)


def _build_url(method):
    """ Build Slack api url

    :param method: slack api call method
    :return: final slack api call url
    """
    return '%s/%s' % (slack.api_base_url, method)


def _parse_response(response):
    """ Parsing response to json

    :param response: slack api response
    :return: parsing json result
    """
    try:
        response = json.loads(response.text)
    except ValueError as e:
        response = {'ok': False, 'error': e}
    return response


def slack_reuqest(token, request="api.test", post_data=None):
    """ POST request to the Slack Web API

    :param token: your authentification token
    :param request: the method to call from the Slack API
                - ex) 'chat.postMessage'
                - https://api.slack.com/methods
    :param post_data:
    :return:
    """
    files = None
    url = 'https://slack.com/api/{0}'.format(request)

    post_data = post_data or {}
    post_data['token'] = token
    return requests.post(url, data=post_data, files=files)


class Server(object):
    def __init__(self, token):
        self.token = token
        # self.connect = connect
        # print('Sever.__init__')
        # print('  token: ', token)
        # print('  connect: ', connect)

    def api_call(self, method, **kwargs):
        """ Call the Slack Web API

        Documented here: https://api.slack.com/web

        :param self:
        :param method:
        :param kwargs:
        :return:
        """
        return slack_reuqest(self.token, method, kwargs).text