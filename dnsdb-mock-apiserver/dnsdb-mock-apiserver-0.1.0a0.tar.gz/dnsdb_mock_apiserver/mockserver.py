# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dnsdb_mock_apiserver import errors
from .utils import validate_ip, random_string
import json
import web
import sys
import time

try:
    import thread
except ImportError:
    import _thread as thread
default_remaining_request = 10
max_page_size = 100
total = 100
default_access_token = None
default_search_id = None

users = []

return_error_response = None


def get_user(username, password):
    for user in users:
        if user.username == username and user.password == password:
            return user
    return None


class ApplicationContext(object):
    def __init__(self):
        self.context = {}

    def has_token(self, token):
        return token in self.context.keys()

    def save_token(self, token, user):
        self.context[token] = user

    def put_retrieve_context(self, search_id, retrieve_context):
        self.context[search_id] = retrieve_context

    def get_retrieve_ctx(self, search_id):
        return self.context[search_id]

    def reset(self):
        self.context = {}


class RetrieveContext(object):
    def __init__(self, data):
        self.data = data
        self.total = len(data)


dns_records = [
                  {'host': 'a.com', 'type': 'a', 'value': '1.1.1.1'},
                  {'host': 'b.com', 'type': 'a', 'value': '1.1.1.2'},
                  {'host': 'c.com', 'type': 'a', 'value': '1.1.1.3'},
                  {'host': 'd.com', 'type': 'a', 'value': '1.1.1.4'},
              ] * 100

context = ApplicationContext()

urls = (
    '/api/v1', 'Index',
    '/api/v1/authorize', 'Authorize',
    '/api/v1/dns/search', 'SearchDns',
    '/api/v1/dns/search_all', 'SearchAllDns',
    '/api/v1/dns/retrieve', 'RetrieveDns',
    '/api/v1/resources', 'Resources',
)


def api_processor(handler):
    res = handler()
    if res:
        data = json.dumps(res)
        web.header('Content-Type', 'application/json')
        web.header('Server', 'DnsDB Mock API Server')
        web.header('Content-Length', len(data))
        return data


class Index(object):
    def GET(self):
        api_info = {'message': 'DnsDB Mock Web API', 'version': 1}
        return api_info


class Authorize(object):
    def POST(self):
        if return_error_response:
            raise return_error_response
        i = web.input()
        username = i.get("username")
        password = i.get("password")
        if default_access_token:
            token = default_access_token
        else:
            token = random_string()
        user = get_user(username, password)
        if user:
            data = {
                'success': True,
                'access_token': token,
                'expire_in': 600
            }

            context.save_token(token, user)
            return data
        else:
            raise errors.UnauthorizedError()


class SearchDns(object):
    def GET(self):
        if return_error_response:
            raise return_error_response
        token = web.ctx.env.get('HTTP_ACCESS_TOKEN')
        if not context.has_token(token):
            raise errors.UnauthorizedError()
        user = context.context[token]
        if user.remaining_request <= 0:
            raise errors.CreditsInsufficientError()
        i = web.input()
        domain = i.get('domain')
        host = i.get('host')
        ip = i.get('ip')
        dns_type = i.get('type')
        start_position = i.get('from')
        if start_position == '':
            start_position = 0
        try:
            start_position = int(start_position)
        except ValueError:
            raise errors.BadRequestError(errors.FROM_VALUE_ERROR)
        if start_position < 0 or start_position > 9970:
            raise errors.BadRequestError(errors.FROM_VALUE_ERROR)

        if ip:
            if not validate_ip(ip):
                raise errors.BadRequestError(errors.IP_VALUE_ERROR)
        if domain is None and ip is None and host is None:
            raise errors.BadRequestError(errors.MISSING_QUERY_ERROR)
        total = len(dns_records)
        data = dns_records[start_position:start_position + 30]
        user.remaining_request -= 1
        return {'success': True, 'data': data, 'remaining_request': user.remaining_request, 'total': total}


class SearchAllDns(object):
    def GET(self):
        if return_error_response:
            raise return_error_response
        token = web.ctx.env.get('HTTP_ACCESS_TOKEN')
        if not context.has_token(token):
            raise errors.UnauthorizedError()
        if default_search_id:
            search_id = default_search_id
        else:
            search_id = random_string()
        retrieve_ctx = RetrieveContext(data=dns_records)
        context.put_retrieve_context(search_id, retrieve_ctx)
        data = {
            "success": True,
            "total": retrieve_ctx.total,
            "id": search_id
        }
        return data


class RetrieveDns(object):
    def GET(self):
        if return_error_response:
            raise return_error_response
        i = web.input()
        search_id = i.get("id")
        token = web.ctx.env.get('HTTP_ACCESS_TOKEN')
        if not context.has_token(token):
            raise errors.UnauthorizedError()
        user = context.context[token]
        retrieve_ctx = context.get_retrieve_ctx(search_id)
        data = retrieve_ctx.data[:max_page_size]
        for record in data:
            retrieve_ctx.data.remove(record)
        if len(data) > 0:
            if user.remaining_request <= 0:
                raise errors.CreditsInsufficientError()
            user.remaining_request -= 1
            return {
                "success": True,
                "total": retrieve_ctx.total,
                "data": data,
                'remaining_request': user.remaining_request
            }
        else:
            raise errors.NotFoundError()


class Resources(object):
    def GET(self):
        if return_error_response:
            raise return_error_response
        token = web.ctx.env.get('HTTP_ACCESS_TOKEN')
        if not context.has_token(token):
            raise errors.UnauthorizedError()
        user = context.context[token]
        return {'remaining_dns_request': user.remaining_request}


app = web.application(urls, globals())
app.add_processor(api_processor)


def start():
    temp = sys.argv
    sys.argv = []
    thread.start_new_thread(app.run, ())
    time.sleep(0.1)
    sys.argv = temp


def stop():
    app.stop()


def restart():
    stop()
    start()
