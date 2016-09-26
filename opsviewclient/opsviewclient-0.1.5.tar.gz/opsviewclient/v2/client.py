#!/usr/bin/env python
# coding: utf-8

import requests

try:
    import simplejson as json
except ImportError:
    import json

from opsviewclient import exceptions as exc
from opsviewclient.v2 import (
    contacts,
    hosts,
    roles,
    service_checks,
    host_templates,
    attributes,
    time_periods,
    host_groups,
    service_groups,
    notification_methods,
    host_check_commands,
    keywords,
    shared_notification_profiles,
    monitoring_servers,
    netflow_collectors,
    netflow_sources,
    tenancies
)


class Client(object):

    _default_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    def __init__(self, username, password, endpoint):
        if endpoint[-1] == '/':
            self.base_url = endpoint
        else:
            self.base_url = endpoint + '/'

        self._username = username
        self._password = password

        self._auth_failed = False

        self._session = requests.Session()
        self._session.headers = Client._default_headers

        self.contacts = contacts.ContactManager(self)
        self.hosts = hosts.HostManager(self)
        self.roles = roles.RoleManager(self)
        self.service_checks = service_checks.ServiceCheckManager(self)
        self.host_templates = host_templates.HostTemplateManager(self)
        self.attributes = attributes.AttributeManager(self)
        self.time_periods = time_periods.TimePeriodManager(self)
        self.host_groups = host_groups.HostGroupManager(self)
        self.service_groups = service_groups.ServiceGroupManager(self)
        self.notification_methods = \
            notification_methods.NotificationMethodManager(self)

        self.host_check_commands = \
            host_check_commands.HostCheckCommandManager(self)

        self.keywords = keywords.KeywordManager(self)
        self.shared_notification_profiles = \
            shared_notification_profiles.SharedNotificationProfileManager(self)

        self.monitoring_servers = \
            monitoring_servers.MonitoringServerManager(self)

        self.netflow_collectors = \
            netflow_collectors.NetflowCollectorManager(self)

        self.netflow_sources = \
            netflow_sources.NetflowSourceManager(self)

        self.tenancies = tenancies.TenancyManager(self)

        self._authenticate()

    def _authenticate(self):
        # Clear the authenticated headers
        self._session.headers.pop('X-Opsview-Username', None)
        self._session.headers.pop('X-Opsview-Token', None)

        payload = {
            'username': self._username,
            'password': self._password,
        }

        response = self._request('POST', 'login', data=payload)

        try:
            token = response['token']
        except Exception as e:
            raise e

        self._session.headers['X-Opsview-Username'] = self._username
        self._session.headers['X-Opsview-Token'] = token

    def _url(self, path):
        if path[0] == '/':
            path = path[1:]

        return self.base_url + path

    def _request(self, method, path, data=None, params=None, expected=[200]):

        if data is not None:
            data = json.dumps(data)

        response = self._session.request(method=method, url=self._url(path),
                                         data=data, params=params)

        if response.status_code not in expected:
            raise exc.OpsviewClientException('Unexpected response: ',
                                             response.text)

        return response.json()

    def get(self, url, **kwds):
        return self._request('GET', url, **kwds)

    def post(self, url, **kwds):
        return self._request('POST', url, **kwds)

    def put(self, url, **kwds):
        return self._request('PUT', url, **kwds)

    def delete(self, url, **kwds):
        return self._request('DELETE', url, **kwds)

    def reload(self):
        return self.post('/reload')
