# Copyright 2013 Rackspace Hosting
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

import pprint

import six

from novaclient import api_versions
from novaclient import base
from novaclient import exceptions
from novaclient.i18n import _
from novaclient.openstack.common import cliutils
from novaclient import utils


class InstanceActionManager(base.ManagerWithFind):
    resource_class = base.Resource

    def get(self, server, request_id):
        """
        Get details of an action performed on an instance.

        :param request_id: The request_id of the action to get.
        """
        return self._get("/servers/%s/os-instance-actions/%s" %
                         (base.getid(server), request_id), 'instanceAction')

    def list(self, server):
        """
        Get a list of actions performed on a server.
        """
        return self._list('/servers/%s/os-instance-actions' %
                          base.getid(server), 'instanceActions')


@api_versions.wraps("2.0", "2.20")
def _find_server(cs, args):
    return utils.find_resource(cs.servers, args.server)


@api_versions.wraps("2.21")
def _find_server(cs, args):
    try:
        return utils.find_resource(cs.servers, args.server,
                                   wrap_exception=False)
    except exceptions.NoUniqueMatch as e:
        raise exceptions.CommandError(six.text_type(e))
    except exceptions.NotFound:
        # The server can be deleted
        return args.server


@cliutils.arg(
    'server',
    metavar='<server>',
    help=_('Name or UUID of the server to show actions for.'),
    start_version="2.0", end_version="2.20")
@cliutils.arg(
    'server',
    metavar='<server>',
    help=_('Name or UUID of the server to show actions for. Only UUID can be '
           'used to show actions for a deleted server.'),
    start_version="2.21")
@cliutils.arg(
    'request_id',
    metavar='<request_id>',
    help=_('Request ID of the action to get.'))
def do_instance_action(cs, args):
    """Show an action."""
    server = _find_server(cs, args)
    action_resource = cs.instance_action.get(server, args.request_id)
    action = action_resource._info
    if 'events' in action:
        action['events'] = pprint.pformat(action['events'])
    utils.print_dict(action)


@cliutils.arg(
    'server',
    metavar='<server>',
    help=_('Name or UUID of the server to list actions for.'),
    start_version="2.0", end_version="2.20")
@cliutils.arg(
    'server',
    metavar='<server>',
    help=_('Name or UUID of the server to list actions for. Only UUID can be '
           'used to list actions on a deleted server.'),
    start_version="2.21")
def do_instance_action_list(cs, args):
    """List actions on a server."""
    server = _find_server(cs, args)
    actions = cs.instance_action.list(server)
    utils.print_list(actions,
                     ['Action', 'Request_ID', 'Message', 'Start_Time'],
                     sortby_index=3)
