# -*- coding: utf-8 -*-
# Copyright 2013-2015 eNovance <licensing@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import oslo_messaging
from oslo_messaging import serializer as oslo_serializer

DEFAULT_URL = "__default__"
TRANSPORTS = {}
_SERIALIZER = oslo_serializer.JsonPayloadSerializer()


def setup():
    oslo_messaging.set_transport_defaults('aodh')


def get_transport(conf, url=None, optional=False, cache=True):
    """Initialise the oslo_messaging layer."""
    global TRANSPORTS, DEFAULT_URL
    cache_key = url or DEFAULT_URL
    transport = TRANSPORTS.get(cache_key)
    if not transport or not cache:
        try:
            transport = oslo_messaging.get_transport(conf, url)
        except (oslo_messaging.InvalidTransportURL,
                oslo_messaging.DriverLoadFailure):
            if not optional or url:
                # NOTE(sileht): oslo_messaging is configured but unloadable
                # so reraise the exception
                raise
            return None
        else:
            if cache:
                TRANSPORTS[cache_key] = transport
    return transport


def get_rpc_server(conf, transport, topic, endpoint):
    """Return a configured oslo_messaging rpc server."""
    target = oslo_messaging.Target(server=conf.host, topic=topic)
    return oslo_messaging.get_rpc_server(transport, target,
                                         [endpoint], executor='threading',
                                         serializer=_SERIALIZER)


def get_rpc_client(transport, retry=None, **kwargs):
    """Return a configured oslo_messaging RPCClient."""
    target = oslo_messaging.Target(**kwargs)
    return oslo_messaging.RPCClient(transport, target,
                                    serializer=_SERIALIZER,
                                    retry=retry)


def get_notification_listener(transport, targets, endpoints,
                              allow_requeue=False):
    """Return a configured oslo_messaging notification listener."""
    return oslo_messaging.get_notification_listener(
        transport, targets, endpoints, executor='threading',
        allow_requeue=allow_requeue)


def get_notifier(transport, publisher_id):
    """Return a configured oslo_messaging notifier."""
    notifier = oslo_messaging.Notifier(transport, serializer=_SERIALIZER)
    return notifier.prepare(publisher_id=publisher_id)
