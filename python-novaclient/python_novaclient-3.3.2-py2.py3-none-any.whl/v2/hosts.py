# Copyright 2011 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
host interface (1.1 extension).
"""
from novaclient import base


class Host(base.Resource):
    def __repr__(self):
        return "<Host: %s>" % self.host

    def _add_details(self, info):
        dico = 'resource' in info and info['resource'] or info
        for (k, v) in dico.items():
            setattr(self, k, v)

    def update(self, values):
        return self.manager.update(self.host, values)

    def startup(self):
        return self.manager.host_action(self.host, 'startup')

    def shutdown(self):
        return self.manager.host_action(self.host, 'shutdown')

    def reboot(self):
        return self.manager.host_action(self.host, 'reboot')

    @property
    def host_name(self):
        return self.host

    @host_name.setter
    def host_name(self, value):
        # A host from hosts.list() has the attribute "host_name" instead of
        # "host." This sets "host" if that's the case. Even though it doesn't
        # exactly mirror the response format, it enables users to work with
        # host objects from list and non-list operations interchangeably.
        self.host = value


class HostManager(base.ManagerWithFind):
    resource_class = Host

    def get(self, host):
        """
        Describes cpu/memory/hdd info for host.

        :param host: destination host name.
        """
        return self._list("/os-hosts/%s" % host, "host")

    def update(self, host, values):
        """Update status or maintenance mode for the host."""
        return self._update("/os-hosts/%s" % host, values)

    def host_action(self, host, action):
        """
        Perform an action on a host.

        :param host: The host to perform an action
        :param actiob: The action to perform
        returns: An instance of novaclient.base.TupleWithMeta
        """
        url = '/os-hosts/{0}/{1}'.format(host, action)
        resp, body = self.api.client.get(url)
        return base.TupleWithMeta((resp, body), resp)

    def list(self, zone=None):
        url = '/os-hosts'
        if zone:
            url = '/os-hosts?zone=%s' % zone
        return self._list(url, "hosts")

    list_all = list
