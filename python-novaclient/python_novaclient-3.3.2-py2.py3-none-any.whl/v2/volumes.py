# Copyright 2011 Denali Systems, Inc.
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
Volume interface (1.1 extension).
"""

import warnings

import six
from six.moves.urllib import parse

from novaclient import base


class Volume(base.Resource):
    """
    DEPRECATED: A volume is an extra block level storage to the OpenStack
    instances.
    """
    NAME_ATTR = 'display_name'

    def __repr__(self):
        return "<Volume: %s>" % self.id

    def delete(self):
        """
        DEPRECATED: Delete this volume.

        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self.manager.delete(self)


class VolumeManager(base.ManagerWithFind):
    """
    DEPRECATED: Manage :class:`Volume` resources.
    """
    resource_class = Volume

    def create(self, size, snapshot_id=None, display_name=None,
               display_description=None, volume_type=None,
               availability_zone=None, imageRef=None):
        """
        DEPRECATED: Create a volume.

        :param size: Size of volume in GB
        :param snapshot_id: ID of the snapshot
        :param display_name: Name of the volume
        :param display_description: Description of the volume
        :param volume_type: Type of volume
        :param availability_zone: Availability Zone for volume
        :rtype: :class:`Volume`
        :param imageRef: reference to an image stored in glance
        """
        warnings.warn('The novaclient.v2.volumes.VolumeManager.create() '
                      'method is deprecated and will be removed after Nova '
                      '13.0.0 is released. Use python-cinderclient or '
                      'python-openstacksdk instead.', DeprecationWarning)
        # NOTE(melwitt): Ensure we use the volume endpoint for this call
        with self.alternate_service_type(
                'volumev2', allowed_types=('volume', 'volumev2')):
            body = {'volume': {'size': size,
                               'snapshot_id': snapshot_id,
                               'display_name': display_name,
                               'display_description': display_description,
                               'volume_type': volume_type,
                               'availability_zone': availability_zone,
                               'imageRef': imageRef}}
            return self._create('/volumes', body, 'volume')

    def get(self, volume_id):
        """
        DEPRECATED: Get a volume.

        :param volume_id: The ID of the volume to get.
        :rtype: :class:`Volume`
        """
        warnings.warn('The novaclient.v2.volumes.VolumeManager.get() '
                      'method is deprecated and will be removed after Nova '
                      '13.0.0 is released. Use python-cinderclient or '
                      'python-openstacksdk instead.', DeprecationWarning)
        with self.alternate_service_type(
                'volumev2', allowed_types=('volume', 'volumev2')):
            return self._get("/volumes/%s" % volume_id, "volume")

    def list(self, detailed=True, search_opts=None):
        """
        DEPRECATED: Get a list of all volumes.

        :rtype: list of :class:`Volume`
        """
        warnings.warn('The novaclient.v2.volumes.VolumeManager.list() '
                      'method is deprecated and will be removed after Nova '
                      '13.0.0 is released. Use python-cinderclient or '
                      'python-openstacksdk instead.', DeprecationWarning)
        with self.alternate_service_type(
                'volumev2', allowed_types=('volume', 'volumev2')):
            search_opts = search_opts or {}

            if 'name' in search_opts.keys():
                search_opts['display_name'] = search_opts.pop('name')

            qparams = dict((k, v) for (k, v) in
                           six.iteritems(search_opts) if v)

            query_str = '?%s' % parse.urlencode(qparams) if qparams else ''

            if detailed is True:
                return self._list("/volumes/detail%s" % query_str, "volumes")
            else:
                return self._list("/volumes%s" % query_str, "volumes")

    def delete(self, volume):
        """
        DEPRECATED: Delete a volume.

        :param volume: The :class:`Volume` to delete.
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        warnings.warn('The novaclient.v2.volumes.VolumeManager.delete() '
                      'method is deprecated and will be removed after Nova '
                      '13.0.0 is released. Use python-cinderclient or '
                      'python-openstacksdk instead.', DeprecationWarning)
        with self.alternate_service_type(
                'volumev2', allowed_types=('volume', 'volumev2')):
            return self._delete("/volumes/%s" % base.getid(volume))

    def create_server_volume(self, server_id, volume_id, device=None):
        """
        Attach a volume identified by the volume ID to the given server ID

        :param server_id: The ID of the server
        :param volume_id: The ID of the volume to attach.
        :param device: The device name (optional)
        :rtype: :class:`Volume`
        """
        body = {'volumeAttachment': {'volumeId': volume_id}}
        if device is not None:
            body['volumeAttachment']['device'] = device
        return self._create("/servers/%s/os-volume_attachments" % server_id,
                            body, "volumeAttachment")

    def update_server_volume(self, server_id, attachment_id, new_volume_id):
        """
        Update the volume identified by the attachment ID, that is attached to
        the given server ID

        :param server_id: The ID of the server
        :param attachment_id: The ID of the attachment
        :param new_volume_id: The ID of the new volume to attach
        :rtype: :class:`Volume`
        """
        body = {'volumeAttachment': {'volumeId': new_volume_id}}
        return self._update("/servers/%s/os-volume_attachments/%s" %
                            (server_id, attachment_id,),
                            body, "volumeAttachment")

    def get_server_volume(self, server_id, attachment_id):
        """
        Get the volume identified by the attachment ID, that is attached to
        the given server ID

        :param server_id: The ID of the server
        :param attachment_id: The ID of the attachment
        :rtype: :class:`Volume`
        """
        return self._get("/servers/%s/os-volume_attachments/%s" % (server_id,
                         attachment_id,), "volumeAttachment")

    def get_server_volumes(self, server_id):
        """
        Get a list of all the attached volumes for the given server ID

        :param server_id: The ID of the server
        :rtype: list of :class:`Volume`
        """
        return self._list("/servers/%s/os-volume_attachments" % server_id,
                          "volumeAttachments")

    def delete_server_volume(self, server_id, attachment_id):
        """
        Detach a volume identified by the attachment ID from the given server

        :param server_id: The ID of the server
        :param attachment_id: The ID of the attachment
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self._delete("/servers/%s/os-volume_attachments/%s" %
                            (server_id, attachment_id,))
