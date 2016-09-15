#!/usr/bin/env python

"""
Copyright 2015 Violin Memory, Inc..

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import datetime
import random

from vmemclient.core import restobject
from vmemclient.core import error


class ReplicationManager01(restobject.SessionNamespace):
    _REPLICATION_BASE_PATH = '/logicalresource/replication'

    def _get_replication_info(self, object_id):
        """Internal worker function for:

            * get_lun_replication_info
        """
        location = '{0}/{1}'.format(self._REPLICATION_BASE_PATH,
                                    object_id)
        ans = self.parent.basic.get(location)
        if not ans['success']:
            raise QueryError(ans.get('msg', str(ans)))

        return ans['data']

    def get_lun_replication_info(self, lun=None, object_id=None):
        """Gets the replication info for the given LUN.

        Arguments:
            object_id -- str

        Returns:
            dict
        """
        if object_id is None:
            object_id = self.parent.lun.lun_name_to_object_id(lun)

        return self._get_replication_info(object_id)

    def _create_replication(self, object_id, server_name,
            server_ip, server_username, server_password, group_name,
            new_target_lun_name, existing_target_lun_object_id,
            target_size, target_thin, target_dedup, target_disable_mirror,
            target_storage_pool_id, continuous_transfer, sync_replica_timemark,
            create_primary_timemark, use_existing_timemark,
            preserve_replication_timemark, initial_time, interval,
            watermark_size, watermark_retry, cdr_size, cdr_storage_pool_id,
            enable_compression, enable_encryption, encryption_option,
            enable_thinray):
        """Internal worker function for:

            * create_lun_replication
        """
        # Constants
        BASE_KEY = 'params'
        SERVER_KEY = 'targetServer'
        DEVICE_KEY = 'targetDevice'
        THIN_KEY = 'thinProvisioning'
        TRANSFER_KEY = 'transferMode'
        TRIGGER_KEY = 'trigger'
        CDR_KEY = 'CDR'
        POLICY_KEY = 'policy'
        ENCRYPTION_KEY = 'encryption'

        # Build request
        location = '{0}/{1}'.format(self._REPLICATION_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY, SERVER_KEY), 'serverName', server_name, 'str'),)
        args += (((BASE_KEY, SERVER_KEY), 'ipaddress', server_ip, 'str'),)
        args += (((BASE_KEY, SERVER_KEY), 'username', server_username, 'str'),)
        args += (((BASE_KEY, SERVER_KEY), 'password', server_password, 'str'),)
        args += (((BASE_KEY,), 'targetGroupName', group_name, 'str'),)
        args += (((BASE_KEY, DEVICE_KEY),
                    'object_id', existing_target_lun_object_id, 'str'),)
        args += (((BASE_KEY, DEVICE_KEY),
                    'name', new_target_lun_name, 'str'),)
        args += (((BASE_KEY, DEVICE_KEY), 'sizeMB', target_size, 'int'),)
        args += (((BASE_KEY, DEVICE_KEY), 'dedup', target_dedup, 'bool'),)
        args += (((BASE_KEY, DEVICE_KEY),
                    'disableMirror', target_disable_mirror, 'bool'),)
        args += (((BASE_KEY, DEVICE_KEY),
                    'storagepoolID', target_storage_pool_id, 'int'),)
        args += (((BASE_KEY, DEVICE_KEY, THIN_KEY),
                    'enabled', target_thin, 'bool'),)
        args += (((BASE_KEY, TRANSFER_KEY),
                    'continuousMode', continuous_transfer, 'bool'),)
        args += (((BASE_KEY, TRANSFER_KEY),
                    'synchronizeReplicaTimemark',
                    sync_replica_timemark, 'bool'),)
        args += (((BASE_KEY, TRANSFER_KEY),
                    'createPrimaryTimemark', create_primary_timemark, 'bool'),)
        args += (((BASE_KEY, TRANSFER_KEY),
                    'useExistingTimemark', use_existing_timemark, 'bool'),)
        args += (((BASE_KEY, TRANSFER_KEY),
                    'preserveReplicationTimemark',
                    preserve_replication_timemark, 'bool'),)
        args += (((BASE_KEY, TRIGGER_KEY),
                    'initialTime', initial_time, 'datetime'),)
        args += (((BASE_KEY, TRIGGER_KEY),
                    'interval', interval, 'str'),)
        args += (((BASE_KEY, TRIGGER_KEY),
                    'watermarkMB', watermark_size, 'int'),)
        args += (((BASE_KEY, TRIGGER_KEY),
                    'watermarkRetry', watermark_retry, 'int'),)
        args += (((BASE_KEY, CDR_KEY), 'sizeMB', cdr_size, 'int'),)
        args += (((BASE_KEY, CDR_KEY),
                    'storagepoolID', cdr_storage_pool_id, 'int'),)
        args += (((BASE_KEY, POLICY_KEY),
                    'compression', enable_compression, 'bool'),)
        args += (((BASE_KEY, POLICY_KEY, ENCRYPTION_KEY),
                    'enabled', enable_encryption, 'bool'),)
        args += (((BASE_KEY, POLICY_KEY, ENCRYPTION_KEY),
                    'option', encryption_option, 'str'),)
        args += (((BASE_KEY, POLICY_KEY),
                    'microscan', enable_thinray, 'bool'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.post(location, data)

    def create_lun_replication(self, source_lun=None,
            server_name=None, server_ip=None,
            server_username=None, server_password=None,
            new_target_lun_name=None, existing_target_lun_name=None,
            target_size=None, target_thin=None, target_dedup=None,
            target_disable_mirror=None, target_storage_pool=None,
            continuous_transfer=None, sync_replica_timemark=None,
            create_primary_timemark=None, use_existing_timemark=None,
            preserve_replication_timemark=None,
            initial_time=None, interval=None,
            watermark_size=None, watermark_retry=None,
            cdr_size=None, cdr_storage_pool=None,
            enable_compression=None, enable_encryption=None,
            encryption_option=None, enable_thinray=None,
            source_lun_object_id=None, existing_target_lun_object_id=None,
            target_storage_pool_id=None, cdr_storage_pool_id=None):
        """Creates a replication policy for the given LUN.

        Arguments:
            source_lun                    -- str
            server_name                   -- str
            server_ip                     -- str
            server_username               -- str
            server_password               -- str
            new_target_lun_name           -- str
            existing_target_lun_name      -- str
            target_size                   -- int
            target_thin                   -- bool
            target_dedup                  -- bool
            target_disable_mirror         -- bool
            target_storage_pool           -- str
            continuous_transfer           -- bool
            sync_replica_timemark         -- bool
            create_primary_timemark       -- bool
            use_existing_timemark         -- bool
            preserve_replication_timemark -- bool
            initial_time                  -- datetime/str
            interval                      -- str
            watermark_size                -- int
            watermark_retry               -- int
            cdr_size                      -- int
            cdr_storage_pool              -- str
            enable_compression            -- bool
            enable_encryption             -- bool
            encryption_option             -- str
            enable_thinray                -- bool
            source_lun_object_id          -- str
            existing_target_lun_object_id -- str
            target_storage_pool_id        -- int
            cdr_storage_pool_id           -- int

        Returns:
            dict
        """
        # Get object ID(s)
        if source_lun_object_id is None:
            source_lun_object_id = self.parent.lun.lun_name_to_object_id(
                    source_lun)
        if (existing_target_lun_object_id is None
                and existing_target_lun_name is not None):
            existing_target_lun_object_id = (
                self.parent.lun.lun_name_to_object_id(
                    existing_target_lun_name,
            ))
        if target_storage_pool_id is None and target_storage_pool is not None:
            target_storage_pool_id = self.parent.pool.storage_pool_name_to_id(
                    target_storage_pool)
        if cdr_storage_pool_id is None and cdr_storage_pool is not None:
            cdr_storage_pool_id = self.parent.pool.storage_pool_name_to_id(
                    cdr_storage_pool)

        return self._create_replication(
            source_lun_object_id, server_name, server_ip,
            server_username, server_password, None,
            new_target_lun_name, existing_target_lun_object_id,
            target_size, target_thin, target_dedup, target_disable_mirror,
            target_storage_pool_id, continuous_transfer, sync_replica_timemark,
            create_primary_timemark, use_existing_timemark,
            preserve_replication_timemark, initial_time, interval,
            watermark_size, watermark_retry, cdr_size, cdr_storage_pool_id,
            enable_compression, enable_encryption, encryption_option,
            enable_thinray,
        )

    def _replication_action(self, action, object_id):
        """Internal worker function for:

            * sync_lun_replication
            * suspend_lun_replication
            * resume_lun_replication
            * stop_lun_replication
        """
        # Constants
        BASE_KEY = 'params'

        # Build request
        location = '{0}/{1}'.format(self._REPLICATION_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY,), 'action', action, 'str'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.put(location, data)

    def sync_lun_replication(self, lun=None, object_id=None):
        """Sync replication for the given LUN.

        Arguments:
            lun       -- str
            object_id -- str

        Returns:
            dict
        """
        if object_id is None:
            object_id = self.parent.lun.lun_name_to_object_id(lun)

        return self._replication_action('sync', object_id)

    def suspend_lun_replication(self, lun=None, object_id=None):
        """Suspend replication for the given LUN.

        Arguments:
            lun       -- str
            object_id -- str

        Returns:
            dict
        """
        if object_id is None:
            object_id = self.parent.lun.lun_name_to_object_id(lun)

        return self._replication_action('suspend', object_id)

    def resume_lun_replication(self, lun=None, object_id=None):
        """Resume replication for the given LUN.

        Arguments:
            lun       -- str
            object_id -- str

        Returns:
            dict
        """
        if object_id is None:
            object_id = self.parent.lun.lun_name_to_object_id(lun)

        return self._replication_action('resume', object_id)

    def stop_lun_replication(self, lun=None, object_id=None):
        """Stop replication for the given LUN.

        Arguments:
            lun       -- str
            object_id -- str

        Returns:
            dict
        """
        if object_id is None:
            object_id = self.parent.lun.lun_name_to_object_id(lun)

        return self._replication_action('stop', object_id)

    def _promote_replication_target(self, object_id, force):
        """Internal worker function for:

            * promote_lun_replication
        """
        # Constants
        BASE_KEY = 'params'

        # Build request
        location = '{0}/{1}'.format(self._REPLICATION_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY,), 'action', 'promote', 'str'),)
        args += (((BASE_KEY,), 'force', force, 'bool'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.put(location, data)

    def promote_lun_replication(self, lun=None, force=None, object_id=None):
        """Promotes the replication LUN for the given source LUN.

        This will also delete the replication policy for the source LUN.

        Arguments:
            lun       -- str
            force     -- bool
            object_id -- str

        Returns:
            dict
        """
        if object_id is None:
            object_id = self.parent.lun.lun_name_to_object_id(lun)

        return self._promote_replication_target(object_id, force)

    def _delete_replication_target(self, object_id, force):
        """Internal worker function for:

            * delete_lun_replication
        """
        # Constants
        BASE_KEY = 'params'

        # Build request
        location = '{0}/{1}'.format(self._REPLICATION_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY,), 'force', force, 'bool'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.delete(location, data)

    def delete_lun_replication(self, lun=None, force=None, object_id=None):
        """Deletes the replication policy for the given LUN.

        Arguments:
            lun       -- str
            force     -- bool
            object_id -- str

        Returns:
            dict
        """
        if object_id is None:
            object_id = self.parent.lun.lun_name_to_object_id(lun)

        return self._delete_replication_target(object_id, force)

    def replicate_lun_to_lun(self, source_lun=None,
                             destination_lun=None, size=None, dedup=None,
                             thin=None, storage_pool=None,
                             source_lun_object_id=None, storage_pool_id=None):
        """Wrapper function to replicate from LUN <src> to LUN <dest>.

        A SRA is created for the source LUN if it does not already exist.

        Arguments:
            source_lun           -- string.  The source LUN to copy.
            destination_lun      -- string.  The destination LUN to copy to.
            size                 -- int.  The size of the LUN (in MB).
            dedup                -- bool.  If the dedup flag should be set.
            thin                 -- bool.  If the thin flag should be set.
            storage_pool         -- string.  The storage pool name.
            source_lun_object_id -- string.  The source LUN's object ID.
            storage_pool_id      -- int.  The storage pool's ID.

        Returns:
            dict
        """
        # Constants
        LAST_SYNC = 'lastSuccessfulSync'
        TIME_ESTIMATE = 'estimatedTimeRemaining'

        # Internal exceptions to end the replication procedure
        class ReplicationError(Exception):
            pass

        class ReplicationTimeout(ReplicationError):
            def __init__(self, action, msg):
                super(ReplicationTimeout, self).__init__(
                    'Timeout {0}; last error message: {1}'.format(
                        action, msg))

        # Perform ID lookups
        if source_lun_object_id is None:
            source_lun_object_id = self.parent.lun.lun_name_to_object_id(
                    source_lun)
        if storage_pool_id is None and storage_pool is not None:
            storage_pool_id = self.parent.pool.storage_pool_name_to_id(
                    storage_pool)

        # Variables
        size = int(size)
        return_status = {'msg': 'Replication completed ok', 'success': True}
        step_timeout = datetime.timedelta(seconds=10)

        # Perform the replication
        try:
            # The destination should not already exist
            try:
                dst_id = self.parent.lun.lun_name_to_object_id(destination_lun)
            except error.NoMatchingObjectIdError:
                pass
            else:
                raise ReplicationError('Destination LUN {0} exists'.format(
                                       destination_lun))

            # Make sure there is a SRA for the source LUN
            if not self.parent.snapshot.lun_has_a_snapshot_resource(
                    source_lun, source_lun_object_id):
                source_lun_info = self.parent.lun.get_lun_info(
                        source_lun, source_lun_object_id)
                ans = self.parent.snapshot.create_snapshot_resource(
                        source_lun, source_lun_info['size_mb'], False,
                        'preserveAll', False,
                        storage_pool_id=storage_pool_id)
                if not ans['success']:
                    raise ReplicationError('Failed to create SRA: {0}'.format(
                                           ans['msg']))

            # Create the replication policy
            start = datetime.datetime.now()
            initial_time = start + datetime.timedelta(days=365)
            while True:
                ans = self.create_lun_replication(
                    source_lun_object_id=source_lun_object_id,
                    new_target_lun_name=destination_lun,
                    target_size=size,
                    target_thin=thin,
                    target_dedup=dedup,
                    target_storage_pool_id=storage_pool_id,
                    continuous_transfer=False,
                    preserve_replication_timemark=False,
                    use_existing_timemark=False,
                    initial_time=initial_time,
                    interval='24H',
                    enable_compression=False,
                    enable_encryption=False,
                    enable_thinray=False,
                )
                if ans['success']:
                    break
                if datetime.datetime.now() - start >= step_timeout:
                    raise ReplicationTimeout('creating replication policy',
                                             ans['msg'])

            # Suspend the replication (allows promotion / deletion)
            start = datetime.datetime.now()
            while True:
                ans = self.suspend_lun_replication(source_lun,
                                                   source_lun_object_id)
                if ans['success']:
                    break
                if datetime.datetime.now() - start >= step_timeout:
                    raise ReplicationTimeout('stopping replication',
                                             ans['msg'])

            # Now, perform the sync
            start = datetime.datetime.now()
            while True:
                ans = self.sync_lun_replication(source_lun,
                                                source_lun_object_id)
                if ans['success']:
                    break
                if datetime.datetime.now() - start >= step_timeout:
                    raise ReplicationTimeout('syncing replication',
                                             ans['msg'])

            # Wait for the last successful sync time to be meaningful
            start = datetime.datetime.now()
            while True:
                ans = self.get_lun_replication_info(source_lun,
                                                    source_lun_object_id)
                if ans['replication'][TIME_ESTIMATE]:
                    continue
                if ans['replication'][LAST_SYNC] != 'N/A':
                    return_status['sync_time'] = (datetime.datetime.now()
                                                  - start)
                    break

            # Promote the replication LUN
            start = datetime.datetime.now()
            while True:
                ans = self.promote_lun_replication(source_lun, True,
                                                   source_lun_object_id)
                if ans['success']:
                    break
                if datetime.datetime.now() - start >= step_timeout:
                    raise ReplicationTimeout('promoting replication',
                                             ans['msg'])
        except ReplicationError as e:
            return_status = {'success': False, 'msg': str(e)}

            # Cleanup
            ans = self.get_lun_replication_info(source_lun,
                                                source_lun_object_id)
            if 'replication' in ans:
                if not ans['replication']['suspended']:
                    self.suspend_lun_replication(source_lun,
                                                 source_lun_object_id)
                self.delete_lun_replication(source_lun, True,
                                            source_lun_object_id)

        # Done
        return return_status

    def replicate_snapshot_to_lun(
                self, source_lun=None, source_snapshot_comment=None,
                destination_lun=None, size=None, dedup=None, thin=None,
                storage_pool=None, source_lun_object_id=None,
                storage_pool_id=None):
        """Wrapper function to replicate a LUN's snapshot to a new LUN.

        Note:  Usage of this function requires that available space be at
               least the size of the original LUN plus the size of the LUN
               that you intend to have at the end.  The current implementation
               of this is that a LUN is first created from the given snapshot,
               then the new LUN (with the desired new size) is created as a
               replication target of that newly created LUN, and finally the
               contents can be replicated over.

        Arguments:
            source_lun              -- string.  The source LUN to copy.
            source_snapshot_comment -- string.  The snapshot comment.
            destination_lun         -- string.  The destination LUN to copy to.
            size                    -- int.  The size of the LUN (in MB).
            dedup                   -- bool.  If the dedup flag should be set.
            thin                    -- bool.  If the thin flag should be set.
            storage_pool            -- string.  The storage pool name.
            source_lun_object_id    -- string.  The source LUN's object ID.
            storage_pool_id         -- int.  The storage pool's ID.

        Returns:
            dict
        """
        # Internal exceptions to end the replication procedure
        class ReplicationError(Exception):
            pass

        class ReplicationTimeout(ReplicationError):
            def __init__(self, action, msg):
                super(ReplicationTimeout, self).__init__(
                    'Timeout {0}; last error message: {1}'.format(
                        action, msg))

        # Variables
        size = int(size)
        return_status = {}
        temp_lun_name = None
        temp_lun_oid = None
        step_timeout = datetime.timedelta(seconds=10)

        # Perform ID lookups
        if source_lun_object_id is None:
            source_lun_object_id = self.parent.lun.lun_name_to_object_id(
                    source_lun)
        if storage_pool_id is None and storage_pool is not None:
            storage_pool_id = self.parent.pool.storage_pool_name_to_id(
                    storage_pool)

        # Perform the replication
        try:
            # The destination should not already exist
            try:
                dst_id = self.parent.lun.lun_name_to_object_id(destination_lun)
            except error.NoMatchingObjectIdError:
                pass
            else:
                raise ReplicationError('Destination LUN {0} exists'.format(
                                       destination_lun))

            # Determine a suitable / unused temp LUN name
            choices = ('abcdefghijklmnopqrstuvwxyz' +
                       'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
                       '1234567890')
            luns = set(x['name'] for x in self.parent.lun.get_luns())
            while True:
                temp_lun_name = 'snaprep_{0}'.format(
                        ''.join(random.choice(choices)
                                for x in xrange(12)))
                if temp_lun_name not in luns:
                    break

            # Create a temp LUN from the snapshot
            start = datetime.datetime.now()
            while True:
                ans = self.parent.lun.copy_snapshot_to_new_lun(
                        source_lun_object_id=source_lun_object_id,
                        source_snapshot_comment=source_snapshot_comment,
                        destination=temp_lun_name,
                        include_data=False,
                        storage_pool_id=storage_pool_id,
                )
                if ans['success']:
                    temp_lun_oid = ans['object_id']
                    break
                if datetime.datetime.now() - start >= step_timeout:
                    raise ReplicationTimeout('creating temp LUN from snapshot',
                                             ans['msg'])

            # Wait for the snapshot copy to complete
            while True:
                status = self.parent.snapshot.get_snapshot_copy_status(
                            source_lun, source_lun_object_id)
                if status[0] is None:
                    continue
                if status[0] != temp_lun_oid or status[2] == 100:
                    break

            # Replicate from the new temp LUN to the destination LUN
            return_status = self.replicate_lun_to_lun(
                    temp_lun_name, destination_lun, size, dedup, thin,
                    storage_pool, source_lun_object_id, storage_pool_id)
        except ReplicationError as e:
            return_status = {'success': False, 'msg': str(e)}
        finally:
            if temp_lun_oid is not None:
                self.parent.lun.delete_lun(temp_lun_name, True, temp_lun_oid)

        # Done
        return return_status
