# -*- coding: utf-8 -*-
import requests

from chatfirst.utils import actually_bytes


# class ChatfirstCall(object):
#     def __init__(self):
#         self.token = None
#         self.host = "https://ch-message-processor-test.azurewebsites.net/"
#         self.version = "v1"
#
#     def init_app(self, app):
#         self.token = app.config['CHATFIRST_USERTOKEN']
#
#     def get(self, method, params=None, headers=None):
#         h = dict() if headers is None else headers
#         h['Authorization'] = "Basic {token}".format(token=b64encode(self.token + ":"))
#         h["Content-Type"] = "application/json"
#
#         url = self.host + self.version + method
#
#         try:
#             res = requests.get(url, params=params, headers=h)
#         except:
#             raise ClientException("Unable to perform Core GET request", 400)
#
#         if res.status_code != 200:
#             print res.text
#             raise ClientException("{method}: Bad Core GET status code".format(method=method), res.status_code)
#         return res.json()
#
#     def post(self, method, data=None, json=None, headers=None):
#         h = dict() if headers is None else headers
#         h['Authorization'] = "Basic {token}".format(token=b64encode(self.token + ":"))
#         h["Content-Type"] = "application/json"
#
#         url = self.host + self.version + method
#         try:
#             res = requests.post(url, data=data, json=json, headers=h)
#         except:
#             raise ClientException("Unable to perform Core POST request", 400)
#
#         if res.status_code not in [200, 201, 202]:
#             print res.text
#             raise ClientException("{method}: Bad Core POST status code".format(method=method), res.status_code)
#         return res.json()
#
#     def put(self, method, json=None, headers=None, params=None):
#         h = dict() if headers is None else headers
#         h['Authorization'] = "Basic {token}".format(token=b64encode(self.token + ":"))
#         h["Content-Type"] = "application/json"
#
#         url = self.host + self.version + method
#
#         try:
#             res = requests.put(url, json=json, params=params, headers=h)
#         except:
#             raise ClientException("Unable to perform Core PUT request", 400)
#
#         if res.status_code not in [200, 202, 204]:
#             print res.text
#             raise ClientException("{method}: Bad Core PUT status code".format(method=method), res.status_code)
#         return res.json()
#
#     def delete(self, method, headers=None, params=None):
#         h = dict() if headers is None else headers
#         h['Authorization'] = "Basic {token}".format(token=b64encode(self.token + ":"))
#         h["Content-Type"] = "application/json"
#
#         url = self.host + self.version + method
#
#         try:
#             res = requests.delete(url, params=params, headers=h)
#         except:
#             raise ClientException("Unable to perform Core DELETE request", 400)
#
#         if res.status_code not in [200, 204]:
#             print res.text
#             raise ClientException("{method}: Bad Core DELETE status code".format(method=method), res.status_code)
#         return res.json()
#
#     def bots_get(self):
#         """
#         Fetches user's bots list
#         :return: List of Bot objects
#         """
#         return bots.get(client=self)
#
#     def bots_get_by_name(self, bot_name):
#         """
#         Fetches bot by name
#         :return: Fetched Bot object
#         """
#         return bots.get_by_name(self, bot_name)
#
#     def bots_save(self, bot):
#         """
#         Saves new bot
#         :return: Saves Bot object
#         """
#         return bots.save(self, self.token, bot)
#
#     def bots_update(self, bot):
#         """
#         Updates bot
#         :return: Deleted Bot object
#         """
#         return bots.update(self, bot)
#
#     def bots_delete(self, bot_name):
#         """
#         Deletes bot
#         :return: Deleted Bot object
#         """
#         return bots.delete(self, bot_name)
#
#     def push_tg(self, obj, bot_name=None, user_id=None):
#         """
#         Pushes user in telegram
#         :param bot_name: Name of bot to push from
#         :param user_id: ID of user to push
#         :param obj: ActionResponse object
#         :return:
#         """
#         return push(token=self.token, botname=bot_name, userid=user_id, obj=obj, channel="telegram")
#
#     def push_fb(self, obj, bot_name=None, user_id=None):
#         """
#         Pushes user in Facebook
#         :param bot_name: Name of bot to push from
#         :param user_id: ID of user to push
#         :param obj: ActionResponse object
#         :return:
#         """
#         return push(token=self.token, botname=bot_name, userid=user_id, obj=obj, channel="facebook")
#
#     def push_sms(self, obj, phone=None):
#         """
#         Pushes user by SMS
#         :param obj: ActionResponse object
#         :param phone: User's phone number
#         :return:
#         """
#         for item in obj.messages:
#             try:
#                 sms(phone, item)
#             except:
#                 return False
#         return True

__author__ = 'it@chatfirst.co (Ivan Tertychnyy)'

from .auth import TokenAuth

try:
    import json
except ImportError:
    import simplejson as json


class _DEFAULT(object):
    pass


class ChatfirstError(Exception):
    """
    Base Exception thrown by the Twitter object when there is a
    general error interacting with the API.
    """
    pass


class ChatfirstHTTPError(ChatfirstError):
    """
    Exception thrown by the Chatfirst object when there is an
    HTTP error interacting with chatfirst.co.
    """
    def __init__(self, sc, method, url, data):
        self.sc = sc
        self.method = method
        self.url = url
        self.response_data = json.dumps(data)
        super(ChatfirstHTTPError, self).__init__(str(self))

    def __str__(self):
        return (
            u"Chatfirst sent status %i for URL: %s %s\ndetails: " % (
                self.sc, self.method, self.url) + self.response_data)


class ChatfirstResponse(object):
    """
    Response from a twitter request. Behaves like a list or a string
    (depending on requested format) but it has a few other interesting
    attributes.
    `headers` gives you access to the response headers as an
    httplib.HTTPHeaders instance. You can do
    `response.headers.get('h')` to retrieve a header.
    """

    @property
    def rate_limit_remaining(self):
        """
        Remaining requests in the current rate-limit.
        """
        return int(self.headers.get('X-Rate-Limit-Remaining', "0"))

    @property
    def rate_limit_limit(self):
        """
        The rate limit ceiling for that given request.
        """
        return int(self.headers.get('X-Rate-Limit-Limit', "0"))

    @property
    def rate_limit_reset(self):
        """
        Time in UTC epoch seconds when the rate limit will reset.
        """
        return int(self.headers.get('X-Rate-Limit-Reset', "0"))


class ChatfirstDictResponse(dict, ChatfirstResponse):
    pass


class ChatfirstListResponse(list, ChatfirstResponse):
    pass


def wrap_response(response, headers):
    response_typ = type(response)
    if response_typ is dict:
        res = ChatfirstDictResponse(response)
        res.headers = headers
    elif response_typ is list:
        res = ChatfirstListResponse(response)
        res.headers = headers
    else:
        res = response
    return res


def build_uri(orig_uriparts, kwargs):
    """
    Build the URI from the original uriparts and kwargs. Modifies kwargs.
    """
    uriparts = []
    for uripart in orig_uriparts:
        # If this part matches a keyword argument (starting with _), use
        # the supplied value. Otherwise, just use the part.
        if uripart.startswith("_"):
            part = (str(kwargs.pop(uripart, uripart)))
        else:
            part = uripart
        uriparts.append(part)
    uri = '/'.join(uriparts)

    # If an id kwarg is present and there is no id to fill in in
    # the list of uriparts, assume the id goes at the end.
    id = kwargs.pop('id', None)
    if id:
        uri += "/%s" % (id)

    return uri


class ChatfirstCall(object):
    def __init__(
            self, auth, format, domain, callable_cls, uri="",
            uriparts=None, secure=True, timeout=None, retry=False):
        self.auth = auth
        self.format = format
        self.domain = domain
        self.callable_cls = callable_cls
        self.uri = uri
        self.uriparts = uriparts
        self.secure = secure
        self.timeout = timeout
        self.retry = retry

    def __getattr__(self, k):
        try:
            return object.__getattr__(self, k)
        except AttributeError:
            def extend_call(arg):
                return self.callable_cls(
                    auth=self.auth, format=self.format, domain=self.domain,
                    callable_cls=self.callable_cls,
                    secure=self.secure, uriparts=self.uriparts + (arg,))
            if k == "_":
                return extend_call
            else:
                return extend_call(k)

    def __call__(self, **kwargs):
        kwargs = dict(kwargs)

        method = kwargs.pop('_method', 'GET')
        params = kwargs.pop('_params', dict())
        headers = kwargs.pop('_method', dict())
        jsondata = kwargs.pop('_json', None)
        if jsondata:
            headers['Content-Type'] = 'application/json; charset=UTF-8'

        domain = self.domain
        uri = build_uri(self.uriparts, kwargs)

        secure_str = ''
        if self.secure:
            secure_str = 's'
        url = "http%s://%s/%s" % (secure_str, domain, uri)

        if self.auth:
            headers.update(self.auth.generate_headers())

        try:
            req = requests.request(method, url=url, params=params, headers=headers, json=jsondata)
        except Exception as e:
            raise e
        return self._handle_response(req)

    def _handle_response(self, req):
        sc = req.status_code
        method = req.request.method

        try:
            data = req.json()
        except:
            data = dict(text=req.text.encode("utf-8"))

        if sc not in [200, 201]:
            raise ChatfirstHTTPError(sc, method, req.url, data)

        if len(data) == 0:
            return {}
        else:
            return data


class ChatfirstClient(ChatfirstCall):
    def __init__(
            self, token, domain="api.chatfirst.co", secure=True):
        """
        Create a new twitter API connector.
        Pass an `auth` parameter to use the credentials of a specific
        user. Generally you'll want to pass an `OAuth`
        instance::
            twitter = Twitter(auth=OAuth(
                    token, token_secret, consumer_key, consumer_secret))
        `domain` lets you change the domain you are connecting. By
        default it's `api.twitter.com`.
        If `secure` is False you will connect with HTTP instead of
        HTTPS.
        `api_version` is used to set the base uri. By default it's
        '1.1'.
        If `retry` is True, API rate limits will automatically be
        handled by waiting until the next reset, as indicated by
        the X-Rate-Limit-Reset HTTP header. If retry is an integer,
        it defines the number of retries attempted.
        """
        auth = TokenAuth(token)

        api_version = 'v1'

        uriparts = ()
        if api_version:
            uriparts += (str(api_version),)

        ChatfirstCall.__init__(
            self, auth=auth, format="json", domain=domain,
            callable_cls=ChatfirstCall,
            secure=secure, uriparts=uriparts)


__all__ = ["Chatfirst", "ChatfirstError", "ChatfirstHTTPError", "ChatfirstResponse"]