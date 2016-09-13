"""
Copyright 2015 Brocade Communications Systems, Inc.

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

from pynos.versions.ver_7.ver_7_0_0.yang.brocade_rbridge import brocade_rbridge
import pynos.utilities


class Services(object):
    """
    The Services class holds all relevent methods and attributes for enabling
    and disabling NOS services, such as VRRP.

    Attributes:
        None
    """
    def __init__(self, callback):
        """
        Services object init.

        Args:
            callback: Callback function that will be called for each action.

        Returns:
            Services Object

        Raises:
            None
        """
        self._callback = callback
        self._rbridge = brocade_rbridge(callback=pynos.utilities.return_xml)

    def vrrp(self, **kwargs):
        """Enable or Disable VRRP.

        Args:
            ip_version (str): The IP version ('4' or '6') for which VRRP should
                be enabled/disabled.  Default: `4`.
            enabled (bool): If VRRP should be enabled or disabled.  Default:
                ``True``.
            rbridge_id (str): The rbridge ID of the device on which VRRP will
                be enabled/disabled.  Default: `1`.
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            None

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.39.211', '10.24.39.203']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.bgp.local_asn(rbridge_id='225')
            ...         output = dev.bgp.local_asn(rbridge_id='225',
            ...         enabled=False)
            ...         output = dev.bgp.local_asn(rbridge_id='225',
            ...         ip_version='6')
            ...         output = dev.bgp.local_asn(rbridge_id='225',
            ...         enabled=False, ip_version='6')
            ...         dev.services.vrrp() # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        ip_version = kwargs.pop('ip_version', '4')
        enabled = kwargs.pop('enabled', True)
        rbridge_id = kwargs.pop('rbridge_id', '1')
        callback = kwargs.pop('callback', self._callback)
        vrrp_args = dict(rbridge_id=rbridge_id)
        vrrp_method = 'rbridge_id_protocol_hide_vrrp_holder_vrrp'
        if ip_version == '6':
            vrrp_method = 'rbridge_id_ipv6_proto_vrrpv3_vrrp'
        vrrp = getattr(self._rbridge, vrrp_method)
        config = vrrp(**vrrp_args)
        if not enabled:
            config.find('.//*vrrp').set('operation', 'delete')
        return callback(config)
