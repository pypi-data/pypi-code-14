#
# Copyright 2012 New Dream Network, LLC (DreamHost)
# Copyright 2013 eNovance
# Copyright 2014-2015 Red Hat, Inc
#
# Authors: Doug Hellmann <doug.hellmann@dreamhost.com>
#          Julien Danjou <julien@danjou.info>
#          Eoghan Glynn <eglynn@redhat.com>
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
"""MongoDB storage backend"""

from oslo_log import log
import pymongo

from aodh import storage
from aodh.storage.mongo import utils as pymongo_utils
from aodh.storage import pymongo_base

LOG = log.getLogger(__name__)


class Connection(pymongo_base.Connection):
    """Put the alarm data into a MongoDB database."""

    CONNECTION_POOL = pymongo_utils.ConnectionPool()

    def __init__(self, conf, url):
        self.conf = conf
        # NOTE(jd) Use our own connection pooling on top of the Pymongo one./
        # We need that otherwise we overflow the MongoDB instance with new
        # connection since we instantiate a Pymongo client each time someone
        # requires a new storage connection.
        self.conn = self.CONNECTION_POOL.connect(
            url,
            conf.database.max_retries,
            conf.database.retry_interval)

        # Require MongoDB 2.4 to use $setOnInsert
        if self.conn.server_info()['versionArray'] < [2, 4]:
            raise storage.StorageBadVersion("Need at least MongoDB 2.4")

        connection_options = pymongo.uri_parser.parse_uri(url)
        self.db = getattr(self.conn, connection_options['database'])
        if connection_options.get('username'):
            self.db.authenticate(connection_options['username'],
                                 connection_options['password'])

        # NOTE(jd) Upgrading is just about creating index, so let's do this
        # on connection to be sure at least the TTL is correctly updated if
        # needed.
        self.upgrade()

    @staticmethod
    def update_ttl(ttl, ttl_index_name, index_field, coll):
        """Update or ensure time_to_live indexes.

        :param ttl: time to live in seconds.
        :param ttl_index_name: name of the index we want to update or ensure.
        :param index_field: field with the index that we need to update.
        :param coll: collection which indexes need to be updated.
        """
        indexes = coll.index_information()
        if ttl <= 0:
            if ttl_index_name in indexes:
                coll.drop_index(ttl_index_name)
            return

        if ttl_index_name in indexes:
            return coll.database.command(
                'collMod', coll.name,
                index={'keyPattern': {index_field: pymongo.ASCENDING},
                       'expireAfterSeconds': ttl})

        coll.ensure_index([(index_field, pymongo.ASCENDING)],
                          expireAfterSeconds=ttl,
                          name=ttl_index_name)

    def upgrade(self):
        super(Connection, self).upgrade()
        # Establish indexes
        ttl = self.conf.database.alarm_history_time_to_live
        self.update_ttl(
            ttl, 'alarm_history_ttl', 'timestamp', self.db.alarm_history)

    def clear(self):
        self.conn.drop_database(self.db.name)
        # Connection will be reopened automatically if needed
        self.conn.close()

    def clear_expired_alarm_history_data(self, alarm_history_ttl):
        """Clear expired alarm history data from the backend storage system.

        Clearing occurs according to the time-to-live.

        :param alarm_history_ttl: Number of seconds to keep alarm history
                                  records for.
        """
        LOG.debug("Clearing expired alarm history data is based on native "
                  "MongoDB time to live feature and going in background.")
