"""
   Copyright 2016 Net-Survey

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

import ipaddress
import logging
import netifaces as ni
import platform


class NetworkInterfaces(object):
    """Retrieves host interface information."""

    _ignore_interfaces = ['lo', 'lo0']
    _hostname = platform.node()
    _host_interfaces = {}
    _host_networks = {}
    _interfaces = []
    _interface_dict = {}

    def __init__(self):
        self._interfaces = self._scrub_interfaces(ni.interfaces())
        self._host_interfaces[self._hostname] = {}
        self._host_networks[self._hostname] = {}

    def _scrub_interfaces(self, _ints):
        """Scrub the interfaces.

        Removes unneeded interfaces from the interface list.

        :param _ints: a list of interfaces
        :returns: a list of scrubbed interfaces
        """
        for interface in self._ignore_interfaces:
            if interface in _ints:
                _ints.remove(interface)

        return _ints

    def _get_network(self, _ip, _netmask):
        """Get network for host interface ip.

        Uses ipaddress module to get the network for host interface ip.

        :param _ip: str object of ip address
        :param _netmask: str object of netmask
        :returns: IPv4Network object describing the network/cidr
        """
        _cidr = ipaddress.IPv4Network(u"0.0.0.0/%s" % _netmask).prefixlen
        _host_ip = ipaddress.ip_interface(u"%s/%s" % (_ip, _cidr))
        _network = _host_ip.network

        return _network

    def get_interfaces(self):
        """Populate the interface dict.

        Creates a dict with scrubbed interfaces and ips.
        {'interfaces':
            'eth0':
                'network': '10.0.0.0/24'
                'addresses': [{'addr': '10.0.0.10',
                               'netmask': '255.255.255.0',
                               'gateway': '10.0.0.1'}]
        }

        :returns: a dict of interfaces and ip addresses
        """
        for _interface in self._interfaces:
            _addresses = ni.ifaddresses(_interface)
            if ni.AF_INET in _addresses:
                self._interface_dict[_interface] = {}
                self._interface_dict[_interface]['addresses'] = \
                    _addresses[ni.AF_INET]
                # (Note: ski) addresses will contain a list of ips:
                # primary, secdonary and network will have the
                # calculated network/cidr
                _first_ip = _addresses[ni.AF_INET][0]['addr']
                _first_nm = _addresses[ni.AF_INET][0]['netmask']
                try:
                    self._interface_dict[_interface]['network'] = \
                        str(self._get_network(_first_ip, _first_nm))
                except (ipaddress.AddressValueError,
                        ipaddress.NetmaskValueError, OSError) as e:
                    logging.error("Error retrieving ip "
                                  "interface network: {}".format(str(e)))

        return self._interface_dict

    def get_host_interfaces(self):
        """Populate the host interfaces dict.

        Creates a dict with the hostname as the key.
        {'hostname':
            'interfaces':
                'eth0':
                    'network': '10.0.0.0/24'
                    'addresses': [{'addr': '10.0.0.10',
                                   'netmask': '255.255.255.0',
                                   'gateway': '10.0.0.1'}]
        }

        :returns: a dict of all host interfaces, ips, networks
        """
        self._host_interfaces[self._hostname]['interfaces'] = \
            self.get_interfaces()

        return self._host_interfaces

    def get_host_networks(self):
        """Populate the hsot networks dict.

        Creates a dict with the hostname as the key for all networks.
        {'hostname':
            '10.0.0.1/24':
                'ips': ['10.0.0.10' ,'10.0.0.2']
        }

        :returns: a dict of all host networks and ips on the network
        """
        _interfaces = self.get_host_interfaces()[self._hostname]['interfaces']

        for int in _interfaces:
            _network = _interfaces[int]['network']
            _addresses = _interfaces[int]['addresses']
            self._host_networks[self._hostname][_network] = {}
            self._host_networks[self._hostname][_network]['ips'] = []
            for address in _addresses:
                self._host_networks[self._hostname][_network]['ips']\
                    .append(address['addr'])

        return self._host_networks
